from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from src.config.database import async_session_local, engine
from src.models.user import Base
from src.routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi động: tự động tạo bảng nếu chưa tồn tại
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Tắt server: giải phóng connection pool
    await engine.dispose()


app = FastAPI(
    title="Blog Cá Nhân Chia Sẻ Video Khóa Học API",
    description="API hệ thống blog cá nhân chia sẻ video khóa học",
    version="1.0.0",
    lifespan=lifespan,
)

# Cấu hình CORS cho phép Frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
