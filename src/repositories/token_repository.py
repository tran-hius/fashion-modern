from src.interfaces.token_repo import TokenRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.token import Token
from sqlalchemy import select, update, delete
from datetime import datetime, timezone

class TokenRepository(TokenRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id, token_hash, expires_at):
        token = Token(user_id=user_id, refresh_token=token_hash,expires_at=expires_at)
        await self.session.add(token)
        await self.session.refresh(token)
        return token

    async def get_by_hash(self, token_hash):
        statement = select(Token).where(Token.refresh_token == token_hash)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def revoke(self, token_id):
        statement = update(Token).where(Token.token_id == token_id, Token.is_revoked.is_(False)).values(is_revoked=True)
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.rowcount > 0

    async def revoke_all_by_user(self, user_id: int) -> int:
        statement = update(Token).where(Token.user_id == user_id, Token.is_revoked.is_(False)).values(is_revoked=True)
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.rowcount

    async def delete_expired(self) -> int:
        statement = delete(Token).where(Token.expires_at < datetime.now(timezone.utc))
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.rowcount
    