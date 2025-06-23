from Database.connection import db
import asyncio
from pathlib import Path

class Migrations:
    def __init__(self, db_pool):
        self.pool = db_pool
        self.migrations_dir = Path("Database/Migrations")
    
    async def create_migrations_tracking_table(self):
        try:
            query = """
                    CREATE TABLE IF NOT EXISTS migrations_tracking (
                    id SERIAL PRIMARY KEY,
                    file_name VARCHAR(255) UNIQUE NOT NULL,
                    applied_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'Asia/Kolkata')
                    )
                    """
            async with self.pool.acquire() as conn:
                await conn.execute(query)
                print("Migrations tracking table created")

        except Exception as e:
            print(f"Exception: {e}")
            return None
    
    async def run_pending_migrations(self):
        try:
            await self.create_migrations_tracking_table()

            applied_migrations_query = "SELECT file_name from migrations_tracking"

            async with self.pool.acquire() as conn:
                applied_rows = await conn.fetch(applied_migrations_query)
                applied_migrations = [row['file_name'] for row in applied_rows]

            migrations_files = sorted(self.migrations_dir.glob("*.sql"))

            pending_migrations = [f for f in migrations_files if f.name not in applied_migrations]

            if not pending_migrations:
                print("No pending migrations")
                return
            
            print(f"There are {len(pending_migrations)} pending migrations")

            for file_name in pending_migrations:
                await self.run_migration(file_name)
        
        except Exception as e:
            print(f"Exception: {e}")
            return None
    
    async def run_migration(self, file_name):
        try:
            with open(file_name, 'r') as file:
                sql_content = file.read()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(sql_content)
                    await conn.execute(
                        "INSERT INTO migrations_tracking (file_name) VALUES ($1)",
                        file_name.name
                    )
            print(f"Applied migration {file_name.name}")
        
        except Exception as e:
            print(f"Exception: {e}")
            return None

async def main():
    try:
        await db.connect()

        migration_runner = Migrations(db.pool)

        await migration_runner.run_pending_migrations()

        await db.disconnect()

    except Exception as e:
            print(f"Exception: {e}")
            return None

if __name__=="__main__":
    asyncio.run(main())