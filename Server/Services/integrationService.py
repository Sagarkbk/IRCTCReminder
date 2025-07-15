from Database.connection import get_db_connection
from Services.userService import get_user_by_id
import pendulum
import secrets
from fastapi import HTTPException, status

async def generateLinkingToken(user_id):
    try:
        async with get_db_connection() as conn:
            token = secrets.token_urlsafe(32)
            query = """
                    INSERT INTO google_telegram_link (user_id, token, expires_at)
                    VALUES ($1, $2, $3)
                    """
            expires_at = pendulum.now('UTC').add(minutes=30)
            await conn.execute(
                query,
                user_id,
                token,
                expires_at
            )
            return token
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def linkTelegramAccount(body, user_id, token):
    try:
        async with get_db_connection() as conn:
            update_user_query = """
                    UPDATE users SET telegram_id = $1,
                    telegram_username = $2,
                    telegram_linked_at = $3,
                    last_updated_at = $3
                    WHERE id = $4
                    RETURNING *
                    """
            update_token_query = """
                                UPDATE google_telegram_link SET is_used = $1
                                WHERE user_id = $2 AND token = $3
                                """
            current_time = pendulum.now('UTC')
            user = None
            async with await conn.transaction() as trsc:
                user = await trsc.fetchrow(update_user_query, body.telegram_id, body.telegram_username, current_time, user_id)
                await trsc.execute(update_token_query, True, user_id, token)
            return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def validateTokenAndGetUser(token: str):
    try:
        async with get_db_connection() as conn:
            token_query = "SELECT * FROM google_telegram_link WHERE token = $1"
            token_data = await conn.fetchrow(token_query, token)

            if not token_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token.")
            
            if token_data['is_used']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This token has already been used.")

            if token_data['expires_at'] < pendulum.now('UTC'):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This token has expired.")

            user_id = token_data['user_id']

            user = await get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User associated with this token does not exists.")

            return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)