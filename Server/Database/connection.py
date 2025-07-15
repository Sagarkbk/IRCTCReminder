import asyncpg
import asyncio
import os
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL")
_pool = None

async def init_pool():
    try:
        global _pool
        if _pool is None or _pool._closed:
            if not DATABASE_URL:
                raise ValueError("DATABASE_URL is not available in Environment Variables")
            _pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=2,
                max_size=10,
            )
            print("Connection Pool is created")
        return _pool
    except Exception as e:
        print(f"Exception: {e}")
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
            return
    except Exception as e:
        print(f"Exception: {e}")
        raise

if __name__=="__main__":
    asyncio.run(test_connection())