from Database.connection import get_db_connection
from datetime import datetime, timezone
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
                                    datetime.now(timezone.utc)
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
                                    datetime.now(timezone.utc), 
                                    user_id
                                )
        return dict(result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)