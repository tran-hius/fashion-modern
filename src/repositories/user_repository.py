from src.interfaces.user_repo import UserRepositoryInterface
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

class UserRepository(UserRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: User) -> User:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)

        return data

    async def get_by_id(self, id: int) -> User | None:
        user = await self.session.get(User, id)
        return user

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_google_id(self, google_id):
        statement = select(User).where(User.google_id == google_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 10 ) -> list[User]:
        statement = select(User).order_by(User.id).offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        return list(result.all())

    async def update(
        self,
        id: int,
        data: dict,
    ) -> bool:
        if not data:
            return False
        statement = (update(User).where(User.id == id).values(**data))
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.rowcount > 0

    async def delete(self, id: int) -> bool:
        user = await self.get_by_id(id)

        if user is None:
            return False

        await self.session.delete(user)
        await self.session.commit()

        return True

    
    