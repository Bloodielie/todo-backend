from fastapi import APIRouter

from fastapi import Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapidi import get_dependency

from app.modules.auth.depends import validate_jwt_token
from app.modules.auth.dtos.token import Token, Check, RefreshToken
from app.modules.auth.dtos.user_data import UserData
from app.modules.auth.use_cases.interfaces import IJwtService, IPasswordHashService, IRefreshTokenService
from app.modules.users.use_cases.interfaces import IUserService

router = APIRouter()


@router.post("/sign_in", response_model=Token)
async def login_for_access_token(
    jwt_service=get_dependency(IJwtService),
    user_service=get_dependency(IUserService),
    password_hash_service=get_dependency(IPasswordHashService),
    refresh_token_service=get_dependency(IRefreshTokenService),
    form_data: OAuth2PasswordRequestForm = Depends()
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

    payload_data = {"sub": user.email, "id": user.id}
    access_token = jwt_service.create_access_token(data=payload_data)

    refresh_token = jwt_service.create_refresh_token(data=payload_data)
    deleted_refresh_token = await refresh_token_service.delete_by_user_id(user.id)
    if deleted_refresh_token is None:
        raise HTTPException(status_code=400, detail="Failed to delete refresh token")
    refresh_token_in_db = await refresh_token_service.create(refresh_token, user.id)
    if refresh_token_in_db is None:
        raise HTTPException(status_code=400, detail="Failed to write refresh token")

    return ORJSONResponse({"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})


@router.post("/refresh_token", response_model=Token)
async def update_tokens(
    refresh_token: RefreshToken,
    jwt_service=get_dependency(IJwtService),
    user_service=get_dependency(IUserService),
    refresh_token_service=get_dependency(IRefreshTokenService)
):
    deleted_refresh_token = await refresh_token_service.delete_by_token(token=refresh_token.refresh_token)
    if deleted_refresh_token is None:
        raise HTTPException(status_code=400, detail="Failed to delete refresh token")
    user = await user_service.get_by_id(deleted_refresh_token.user_id)

    payload_data = {"sub": user.email, "id": user.id}
    refresh_token = jwt_service.create_refresh_token(data=payload_data)
    refresh_token_in_db = await refresh_token_service.create(refresh_token, user.id)
    if refresh_token_in_db is None:
        raise HTTPException(status_code=400, detail="Failed to write refresh token")

    access_token = jwt_service.create_access_token(data=payload_data)
    return ORJSONResponse({"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})


@router.post("/register", response_model=Token, status_code=201)
async def register_new_user(
    user_date: UserData,
    jwt_service=get_dependency(IJwtService),
    user_service=get_dependency(IUserService),
    refresh_token_service=get_dependency(IRefreshTokenService)
):
    user = await user_service.create(**user_date.dict())
    if user is None:
        raise HTTPException(status_code=400, detail="Failed to create user")

    payload_data = {"sub": user.email, "id": user.id}
    refresh_token = jwt_service.create_refresh_token(data=payload_data)
    refresh_token_in_db = await refresh_token_service.create(refresh_token, user.id)
    if refresh_token_in_db is None:
        raise HTTPException(status_code=400, detail="Failed to write refresh token")

    access_token = jwt_service.create_access_token(data=payload_data)
    return ORJSONResponse({"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}, 201)


@router.get("/check_token", response_model=Check, status_code=200)
async def check_token(_: str = Depends(validate_jwt_token)):
    return ORJSONResponse(Check(status=True).dict())
