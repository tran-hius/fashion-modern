# src/interfaces/token_repo.py
from abc import ABC, abstractmethod
from datetime import datetime
from src.models.token import Token

class TokenRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, user_id: int, token_hash: str, expires_at: datetime) -> Token: 
        pass

    @abstractmethod
    async def get_by_hash(self, token_hash: str) -> Token | None: 
        pass

    @abstractmethod
    async def revoke(self, token_id: int) -> bool: 
        pass

    @abstractmethod
    async def revoke_all_by_user(self, user_id: int) -> int: 
        pass

    @abstractmethod
    async def delete_expired(self) -> int: 
        pass