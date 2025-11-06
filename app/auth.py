from datetime import datetime, UTC, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)
