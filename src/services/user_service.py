from src.interfaces.user_repo import UserRepositoryInterface
from src.models.user import User
from src.schemas.user import UserUpdate, UserCreate
from src.security.security import hash_password


class UserService:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def get_by_id(self, id: int) -> User | None:
        user = await self.user_repo.get_by_id(id)
        if user is None:
            raise ValueError("Không tìm thấy user")
        return user

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[User]:
        return await self.user_repo.get_all(skip, limit)

    async def create(self, data: UserCreate) -> User:
        user = await self.user_repo.get_by_email(data.email)

        if user:
            raise ValueError("Email đã tồn tại")

        password_hash = hash_password(data.password)

        new_user = User(full_name = data.full_name, email = data.email, hashed_password = password_hash)

        return await self.user_repo.create(new_user)

    async def update(self, id: int, data: UserUpdate) -> User | None:
        update_data = data.model_dump(exclude_unset=True)

        allowed_fields = {
            "full_name",
            "email",
            "address",
            "phone_number",
        }

        if "email" in update_data:
            existing = await self.user_repo.get_by_email(update_data["email"])
            if existing and existing.id != id:
                raise ValueError("Email đã tồn tại")

        user = await self.user_repo.update(
            id=id,
            data=update_data,
            allowed_fields=allowed_fields,
            )

        if user is None:
            raise ValueError("Không tìm thấy user")

        return user

    async def delete(self, id: int) -> bool:
        deleted = await self.user_repo.delete(id)

        if not deleted:
            raise ValueError("Không tìm thấy user")

        return True
    

