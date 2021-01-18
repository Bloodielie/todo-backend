from fastapi import APIRouter, Depends

from app.modules.auth.depends import validate_jwt_token
from app.modules.cards.controller import router as card_router
from app.modules.auth.controller import router as auth_router

main_router = APIRouter()

main_router.include_router(card_router, prefix="/card", tags=["Cards"], dependencies=[Depends(validate_jwt_token)])
main_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
