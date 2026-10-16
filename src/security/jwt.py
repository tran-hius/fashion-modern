import hashlib, secrets, jwt
from datetime import datetime, timedelta, timezone
from src.config.settings import settings

def create_access_token(user_id) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes)
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.algorithm)

def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.algorithm])
    return int(payload["sub"])

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()