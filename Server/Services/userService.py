from Database.connection import get_db_connection
import pendulum
from fastapi import HTTPException, status

async def create_user(userInfo):
    try:
        conn = await get_db_connection()
        query = """
                INSERT INTO users (google_id, email, username, last_updated_at) 
                VALUES ($1, $2, $3, $4) 
                RETURNING *
                """
        result = await conn.fetchrow(
                                    query, 
                                    userInfo.get('sub'), 
                                    userInfo.get('email'), 
                                    userInfo.get('name'), 
                                    pendulum.now('UTC')
                                )
        return dict(result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def get_user_by_id(user_id):
    try:
        conn = await get_db_connection()
        query = """
                SELECT * FROM users WHERE id = $1
                """
        existingUser = await conn.fetchrow(query, user_id)
        return dict(existingUser) if existingUser else None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def get_user_by_google_id(google_id):
    try:
        conn = await get_db_connection()
        query = """
                SELECT * FROM users WHERE google_id = $1
                """
        existingUser = await conn.fetchrow(query, google_id)
        return dict(existingUser) if existingUser else None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def update_user(userInfo, user_id):
    try:
        conn = await get_db_connection()
        query = """
                UPDATE users 
                SET email = $1, username = $2, last_updated_at = $3
                WHERE id = $4
                RETURNING *
                """
        result = await conn.fetchrow(
                                    query, 
                                    userInfo.get('email'), 
                                    userInfo.get('name'), 
                                    pendulum.now('UTC'), 
                                    user_id
                                )
        return dict(result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
async def update_user_settings(user_id, body):
    try:
        conn = await get_db_connection()
        user = await get_user_by_id(user_id)
        calendar_enabled = user['calendar_enabled']
        telegram_enabled = user['telegram_enabled']
        if body.calendar_enabled is not None:
            calendar_enabled = body.calendar_enabled
        if body.telegram_enabled is not None:
            telegram_enabled = body.telegram_enabled
        query = """
                UPDATE users
                SET calendar_enabled = $1, telegram_enabled = $2, last_updated_at = $3
                WHERE id = $4
                RETURNING *
                """
        updated_user = await conn.fetchrow(query, calendar_enabled, telegram_enabled,
                                        pendulum.now('UTC'), user_id)
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)