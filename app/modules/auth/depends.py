from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapidi import get_dependency
from starlette import status

from app.config import API_PATH
from app.modules.auth.use_cases.interfaces import IJwtService
from app.modules.users.dtos.user import User
from app.modules.users.use_cases.interfaces import IUserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PATH}/auth/sign_in")


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def validate_jwt_token(jwt_service=get_dependency(IJwtService), token: str = Depends(oauth2_scheme)) -> str:
    payload = jwt_service.decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    return username


async def get_current_user(
    user_service=get_dependency(IUserService), username: str = Depends(validate_jwt_token)
) -> User:
    user = await user_service.get_by_email(username)
    if user is None:
        raise credentials_exception
    return user
