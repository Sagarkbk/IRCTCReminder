import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

async def test_connection():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Successfully connected to local postgres docker container")
        await conn.close()
    except Exception as e:
        print(f"Exception : {e}")

asyncio.run(test_connection())