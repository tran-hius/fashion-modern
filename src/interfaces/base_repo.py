from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")

class BaseRepository(ABC, Generic[T, ID]):

    @abstractmethod
    async def create(self, data: T) -> T:
        pass
    @abstractmethod
    async def get_by_id(self, id: ID) -> T | None:
            pass
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 10) -> list[T]:
            pass
    @abstractmethod
    async def update(self, id: ID, data: T) -> bool:
        pass
    @abstractmethod
    async def delete(self, id: ID) -> bool:
        pass