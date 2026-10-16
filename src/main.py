from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from src.config.database import async_session_local, engine
from src.config.settings import settings
from src.models.user import Base
from src.repositories.token_repository import TokenRepository
from src.routers.auth import router as auth_router
from src.routers.user import router as user_router
from src.dependencies import get_current_user_id


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_local() as session:
        await TokenRepository(session).delete_expired()
    yield
    await engine.dispose()


app = FastAPI(
    title="Blog Cá Nhân Chia Sẻ Video Khóa Học API",
    description="API hệ thống blog cá nhân chia sẻ video khóa học",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router)


@app.get("/health", tags=["Health"])
@app.get("/db-check", tags=["Health"])
async def db_check():
    async with async_session_local() as session:
        result = await session.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": result.scalar(),
        }


@app.get("/auth-check", tags=["Health"], summary="Kiểm tra Access Token đăng nhập")
async def auth_check(user_id: int = Depends(get_current_user_id)):
    return {
        "status": "authenticated",
        "user_id": user_id,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
