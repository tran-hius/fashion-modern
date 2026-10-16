import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_session
from src.models.user import User
from src.repositories.token_repository import TokenRepository
from src.repositories.user_repository import UserRepository
from src.security.jwt import decode_access_token
from src.services.auth_service import AuthService
from src.services.user_service import UserService

bearer = HTTPBearer()


def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_token_repo(session: AsyncSession = Depends(get_session)) -> TokenRepository:
    return TokenRepository(session)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(user_repo)


def get_auth_service(
    token_repo: TokenRepository = Depends(get_token_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> AuthService:
    return AuthService(token_repo, user_repo)


async def get_current_user_id(
    cred: HTTPAuthorizationCredentials = Depends(bearer),
) -> int:
    try:
        return decode_access_token(cred.credentials)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    user_repo: UserRepository = Depends(get_user_repo),
) -> User:
    user = await user_repo.get_by_id(user_id)
    if not user or user.is_blocked or user.is_pending_deletion:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản không khả dụng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user