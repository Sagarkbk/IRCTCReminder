import asyncpg
import asyncio
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

_pool = None

async def init_pool():
    global _pool
    if _pool is not None and not _pool._closed:
        return _pool
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not available in Environment Variables")

    try:
        _pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=2,
                max_size=10,
                command_timeout=60,
            )
        print("Connection Pool is created")
        return _pool
    except Exception as e:
        print(f"Failed to create database connection pool: {e}")
        raise

@asynccontextmanager
async def get_db_connection():
    try:
        pool = await init_pool()
        async with pool.acquire() as conn:
            yield conn
    except Exception as e:
        print(f"Exception: {e}")
        raise

async def close_pool():
    try:
        global _pool
        if _pool and not _pool._closed:
            await _pool.close()
            print("Connection Pool closed")
    except Exception as e:
        print(f"Exception: {e}")
        raise

async def test_connection():
    try:
        async with get_db_connection() as conn:
            result = await conn.fetchrow("SELECT 1 AS test")
            print(f"Result: {result['test']}")
            print("Connected to database")
        await close_pool()
    except Exception as e:
        print(f"Exception: {e}")
        raise

if __name__=="__main__":
    asyncio.run(test_connection())