from fastapi import APIRouter

from fastapi import Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapidi import get_dependency
from app.modules.auth.dtos.token import Token
from app.modules.auth.dtos.user_data import UserData
from app.modules.auth.use_cases.interfaces import IJwtService, IPasswordHashService
from app.modules.users.use_cases.interfaces import IUserService

router = APIRouter()


@router.post("/sign_in", response_model=Token)
async def login_for_access_token(
    jwt_service=get_dependency(IJwtService),
    user_service=get_dependency(IUserService),
    password_hash_service=get_dependency(IPasswordHashService),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await user_service.get_by_email(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not password_hash_service.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt_service.create_access_token(data={"sub": user.email})
    return ORJSONResponse({"access_token": access_token, "token_type": "bearer"})


@router.post("/register", response_model=Token, status_code=201)
async def register_new_user(
    user_date: UserData, jwt_service=get_dependency(IJwtService), user_service=get_dependency(IUserService)
):
    user = await user_service.create(**user_date.dict())
    if user is None:
        raise HTTPException(status_code=400, detail="Failed to create user")
    access_token = jwt_service.create_access_token(data={"sub": user.email})
    return ORJSONResponse({"access_token": access_token, "token_type": "bearer"}, status_code=201)
