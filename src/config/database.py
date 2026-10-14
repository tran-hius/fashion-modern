import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Thiếu DATABASE_URL trong file .env")

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

async_session_local = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session():
    async with async_session_local() as session:
        yield session