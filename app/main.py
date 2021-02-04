from databases import Database
from fastapidi import FastAPIDI, __version__
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.config import TITLE, DESCRIPTION, DB_URL, DB_POOL_MIN_SIZE, DB_POOL_MAX_SIZE, API_PATH
from app.dependencies import configure_dependencies
from app.events import on_startup, on_shutdown
from app.infrastructure.log import configure_logging
from app.infrastructure.urls import main_router

configure_logging()

app = FastAPIDI(title=TITLE, version=__version__, default_response_class=ORJSONResponse, description=DESCRIPTION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database(DB_URL, min_size=DB_POOL_MIN_SIZE, max_size=DB_POOL_MAX_SIZE)

app.container.add_constant(Database, database)

configure_dependencies(app.container)

app.add_event_handler("startup", on_startup(database))
app.add_event_handler("shutdown", on_shutdown(database))

app.include_router(main_router, prefix=API_PATH)
