from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generate JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=720))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "MySecretKey", algorithm="HS256")