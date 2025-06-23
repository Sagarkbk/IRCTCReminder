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
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not defined in Environment Variables")
        self.pool = await asyncpg.create_pool(
            self.DATABASE_URL,
            min_size=2,
            max_size=10
        )
        print("Database connection pool created.")
    
    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            print("Database connection pool closed.")
    
    async def fetch_one(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

db = Database()

async def test_conn_pool():
    try:
        await db.connect()
        result = await db.fetch_one('SELECT 1 AS test')
        print(f"Test query result: {result['test']}")
        print("Connected to database.")
    except Exception as e:
        print("Failed to connect to database. {e}")
        return None

if __name__=="__main__":
    asyncio.run(test_conn_pool())