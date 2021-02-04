from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from jose import jwt, JWTError

from app.config import JWT_TOKEN_EXPIRE_MINUTES, SECRET_KEY, JWT_ALGORITHM
from app.modules.auth.use_cases.interfaces import IJwtService


def _added_exp_to_data(data: Dict[str, Any], minutes: int) -> Dict[str, Any]:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    to_encode.update({"exp": expire})
    return to_encode


class JwtService(IJwtService):
    def create_access_token(self, data: Dict[str, Any]) -> str:
        exp_data = _added_exp_to_data(data, JWT_TOKEN_EXPIRE_MINUTES)
        return jwt.encode(exp_data, SECRET_KEY, algorithm=JWT_ALGORITHM)

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        exp_data = _added_exp_to_data(data, JWT_TOKEN_EXPIRE_MINUTES*100)
        return jwt.encode(exp_data, SECRET_KEY, algorithm=JWT_ALGORITHM)

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except JWTError:
            return None
