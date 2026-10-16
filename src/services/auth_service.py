from src.interfaces.token_repo import TokenRepositoryInterface 
from src.schemas.token import TokenResponse
from src.security.jwt import hash_token, generate_refresh_token, create_access_token
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from src.config.settings import settings
import secrets
from src.security.google_oauth import fetch_google_userinfo
from src.interfaces.user_repo import UserRepositoryInterface
from src.models.user import Role, User

class AuthService:
    def __init__(self, token_repo: TokenRepositoryInterface, user_repo: UserRepositoryInterface):
        self.token_repo = token_repo
        self.user_repo = user_repo

    def _ensure_active(self, user: User) -> None:
        if user.is_blocked or user.is_pending_deletion:
            raise HTTPException(403, "Tài khoản đã bị khóa hoặc đang chờ xóa")

    async def login_with_google(self, code: str) -> TokenResponse:
        info = await fetch_google_userinfo(code)
        if not info.get("email_verified"):
            raise HTTPException(400, "Email chưa được Google xác minh")
        user = await self._get_or_create_google_user(info)
        self._ensure_active(user)
        return await self._issue_tokens(user.id)

    async def _get_or_create_google_user(self, info: dict) -> User:
        user = await self.user_repo.get_by_google_id(info["sub"])
        if user:
            return user

        user = await self.user_repo.get_by_email(info["email"])
        if user:
            await self.user_repo.update(user.id, {"google_id": info["sub"], "is_verify": True})
            user.google_id = info["sub"]
            user.is_verify = True
            return user

        new_user = User(
            email=info["email"],
            full_name=info.get("name") or info["email"].split("@")[0],
            username=await self._generate_username(info["email"]),
            avatar_url=info.get("picture"),
            google_id=info["sub"],
            is_verify=True,
            role=Role.USER,
        )

        return await self.user_repo.create(new_user)

    async def _issue_tokens(self, user_id: int) -> TokenResponse:
        refresh_token = generate_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_days)
        await self.token_repo.create(user_id, hash_token(refresh_token), expires_at)
        return TokenResponse(access_token=create_access_token(user_id), refresh_token=refresh_token)
    
    async def refresh(self, refresh_token: str) -> TokenResponse:
        row = await self.token_repo.get_by_hash(hash_token(refresh_token))

        if not row:
            raise HTTPException(401, "Refresh token không hợp lệ") 

        if row.is_revoked:
            await self.token_repo.revoke_all_by_user(row.user_id)
            raise HTTPException(401, "Token đã bị thu hồi, vui lòng đăng nhập lại")

        if row.expires_at < datetime.now(timezone.utc):
            raise HTTPException(401, "Refresh token đã hết hạn")

        user = await self.user_repo.get_by_id(row.user_id)
        if not user:
            raise HTTPException(401, "Refresh token không hợp lệ")

        self._ensure_active(user)

        # Rotation: thu hồi token cũ, nếu thất bại nghĩa là có request khác đã dùng trước
        if not await self.token_repo.revoke(row.id):
            raise HTTPException(401, "Refresh token không hợp lệ")

        return await self._issue_tokens(row.user_id)

    async def logout(self, refresh_token: str) -> None:
        row = await self.token_repo.get_by_hash(hash_token(refresh_token))
        if row:
            await self.token_repo.revoke(row.id)

    async def logout_all(self, user_id: int) -> None:
        await self.token_repo.revoke_all_by_user(user_id)

    async def _generate_username(self, email: str) -> str:
        base = email.split("@")[0][:80].lower()
        username = base
        while await self.user_repo.get_by_username(username):
            username = f"{base}{secrets.token_hex(2)}"
        return username