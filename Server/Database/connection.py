from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
import os
from .models import Base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

async def test_connection():
    try:
        engine = create_async_engine(DATABASE_URL)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Tables created")
    except Exception as e:
        print(f"Exception : {e}")

if __name__=="__main__":
    asyncio.run(test_connection())