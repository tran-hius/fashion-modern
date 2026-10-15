from fastapi import APIRouter, Depends, HTTPException, status, Query 
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import get_session
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserCreate, UserResponse, UserUpdate, MessageResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_user_service(session: AsyncSession = Depends(get_session),) -> UserService:
    user_repo = UserRepository(session)
    return UserService(user_repo)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return await service.create(data)
    except ValueError as e:
        if str(e) == "Email đã tồn tại":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        raise

@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(id: int, service: UserService = Depends(get_user_service)):
    try:
        return await service.get_by_id(id)
    except ValueError as e:
        if str(e) == "Không tìm thấy user":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        raise
@router.get("/", response_model=list[UserResponse])
async def get_all_users(
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100),
        service: UserService = Depends(get_user_service)
    ):
        return await service.get_all(skip, limit)

@router.patch("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK,)
async def update_user(id: int, data: UserUpdate, service: UserService = Depends(get_user_service)):
    try:
        return await service.update(id, data)
    except ValueError as e:
        if str(e) == "Không tìm thấy user":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        if str(e) == "Email đã tồn tại":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        if str(e).startswith("Không được phép cập nhật:"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        raise

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,)
async def delete_user(
    id: int,
    service: UserService = Depends(get_user_service),
):
    try:
        await service.delete(id)
    except ValueError as e:
        if str(e) == "Không tìm thấy user":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        raise

@router.patch("/{id}/block", response_model=MessageResponse)
async def block_user(id: int, service: UserService = Depends(get_user_service)):
    try:
        await service.block_user(id)
        return {"message": "Khóa user thành công"}
    except ValueError as e:
        if str(e) == "Không tìm thấy user":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.patch("/{id}/unblock", response_model=MessageResponse)
async def unblock_user(id: int, service: UserService = Depends(get_user_service)):
    try:
        await service.unblock_user(id)
        return {"message": "Mở khóa user thành công"}
    except ValueError as e:
        if str(e) == "Không tìm thấy user":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )