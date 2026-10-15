from src.interfaces.token_repo import TokenRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession

class TokenRepository(TokenRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id, token_hash, expires_at):
        return await super().create(user_id, token_hash, expires_at)

    async def get_by_hash(self, token_hash):
        return await super().get_by_hash(token_hash)

    async def revoke(self, token_id):
        return await super().revoke(token_id)

    async def revoke_all_by_user(self, user_id):
        return await super().revoke_all_by_user(user_id)

    async def delete_expired(self):
        return await super().delete_expired()
    