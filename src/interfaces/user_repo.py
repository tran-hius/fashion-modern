from abc import abstractmethod
from src.interfaces.base_repo import BaseRepository
from src.models.user import User

class UserRepositoryInterface(BaseRepository[User, int]):
    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass