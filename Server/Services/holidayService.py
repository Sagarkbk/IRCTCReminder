from Database.connection import get_db_connection
from datetime import datetime, timezone

async def get_existing_holidays(user_id):
    try:
        conn = await get_db_connection()
        query = """
                SELECT * FROM selected_holidays WHERE user_id = $1
                """
        holidays = await conn.fetch(query, user_id)
        return holidays
    except Exception as e:
        raise
    finally:
        await conn.close()

async def add_holidays():
    pass

async def update_holidays():
    pass