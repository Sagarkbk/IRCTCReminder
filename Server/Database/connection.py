import asyncpg
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.pool = None
        self.DATABASE_URL = os.getenv("DATABASE_URL")

    async def connect(self):
        try:
            if not self.DATABASE_URL:
                raise ValueError("DATABASE_URL is not defined in Environment Variables")

            if self.pool and not self.pool._closed:
                print("Connection pool already exists")
                return

            self.pool = await asyncpg.create_pool(
                self.DATABASE_URL,
                min_size=2,
                max_size=10
            )
            print("Database connection pool created.")
        except Exception as e:
            print(f"Failed to create connection pool: {e}")
            raise

    async def disconnect(self):
        if self.pool and not self.pool._closed:
            try:
                await asyncio.wait_for(self.pool.close(), timeout=5.0)
                print("Connection pool closed")
            except asyncio.TimeoutError:
                print("Connection pool close timed out, terminating connections...")
                await self.pool.terminate()
                print("Connection pool terminated")
            except Exception as e:
                print(f"Failed to disconnect connection pool: {e}")
                raise
        else:
            print("There is no existing connection pool to close")
    
    async def execute(self, query, *args):
        try:
            if not self.pool or self.pool._closed:
                await self.connect()
            async with self.pool.acquire() as conn:
                return await conn.execute(query, *args)
        except Exception as e:
            print(f"Exception in execute: {e}")
            raise
    
    async def fetchone(self, query, *args):
        try:
            if not self.pool or self.pool._closed:
                await self.connect()
            async with self.pool.acquire() as conn:
                return await conn.fetchrow(query, *args)
        except Exception as e:
            print(f"Exception in fetchone: {e}")
            raise
    
    async def fetchall(self, query, *args):
        try:
            if not self.pool or self.pool._closed:
                await self.connect()
            async with self.pool.acquire() as conn:
                return await conn.fetch(query, *args)
        except Exception as e:
            print(f"Exception in fetchall: {e}")
            raise

db = Database()

async def test_conn_pool():
    try:
        await db.connect()
        result = await db.fetchone('SELECT 1 AS test')
        print(f"Test query result: {result['test']}")
        print("Connected to database.")
    except Exception as e:
        print(f"Failed to connect to database. {e}")
        return None

if __name__=="__main__":
    asyncio.run(test_conn_pool())