import sqlalchemy
from starlette.config import Config

metadata = sqlalchemy.MetaData()

config = Config(".env")

TITLE = config.get("title", cast=str, default="TODO")
DESCRIPTION = config.get("description", cast=str, default="Test app app")

DB_URL = config.get("db_url", cast=str)
DB_POOL_MIN_SIZE = config.get("db_pool_min_size", cast=int, default=1)
DB_POOL_MAX_SIZE = config.get("db_pool_max_size", cast=int, default=5)

LOG_LEVEL = config.get("log_level", cast=str, default="DEBUG")

API_PATH = config.get("api_path", cast=str, default="/api")

SECRET_KEY = config.get(
    "secret_key", cast=str, default="43579379deee3a467d03566a29425e61c70cba9f18061ac7b4a67c313c70e48b"
)
JWT_ALGORITHM = config.get("jwt_algorithm", cast=str, default="HS256")
JWT_TOKEN_EXPIRE_MINUTES = config.get("jwt_token_expire_minutes", cast=int, default=30)

first_superuser_email = config.get("first_superuser_email", cast=str)
first_superuser_password = config.get("first_superuser_password", cast=str)
