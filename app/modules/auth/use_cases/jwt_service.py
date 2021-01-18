from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from jose import jwt, JWTError

from app.config import JWT_TOKEN_EXPIRE_MINUTES, SECRET_KEY, JWT_ALGORITHM
from app.modules.auth.use_cases.interfaces import IJwtService


class JwtService(IJwtService):
    def create_access_token(self, data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=JWT_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

    def decode_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except JWTError:
            return None
