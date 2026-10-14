
from fastapi import FastAPI
from sqlalchemy import text
from src.config.database import async_session_local

app = FastAPI()


@app.get("/db-check")
async def db_check():
    async with async_session_local() as session:
        result = await session.execute(text("SELECT 1"))

        return {
            "database": result.scalar()
        }
