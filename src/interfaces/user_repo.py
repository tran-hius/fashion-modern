from abc import abstractmethod
from src.interfaces.base_repo import BaseRepository
from src.models.user import User

class UserRepositoryInterface(BaseRepository[User, int]):

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def get_by_google_id(self, google_id: str) -> User | None:
        pass

