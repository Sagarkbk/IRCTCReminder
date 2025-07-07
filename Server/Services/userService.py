from Database.connection import get_db_connection, close_pool
from datetime import datetime, timezone

async def create_user(userInfo):
    try:
        conn = await get_db_connection()
        query = """
                INSERT INTO users (google_id, email, username, last_updated_at) 
                VALUES ($1, $2, $3, $4)
                """
        await conn.execute(query, userInfo.get('sub'), userInfo.get('email'), 
                        userInfo.get('name'), datetime.now(timezone.utc))
        return {"existingUser": False, "newUser": True}
    except Exception as e:
        raise
    finally:
        await close_pool()

async def get_user(userInfo):
    try:
        conn = await get_db_connection()
        query = """
                SELECT * FROM users WHERE google_id = $1 AND email = $2 AND username = $3
                """
        existingUser = await conn.fetchrow(query, userInfo.get('sub'), userInfo.get('email'),
                                        userInfo.get('name'))
        return existingUser
    except Exception as e:
        raise
    finally:
        await close_pool()