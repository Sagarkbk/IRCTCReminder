from Database.connection import get_db_connection
from Services.userService import get_user_by_id
import pendulum
import secrets
from fastapi import HTTPException, status, Depends
from Services.redisService import get_redis
from redis.asyncio import Redis
import json

async def generateLinkingToken(user_id, rds=None):
    try:
        async with get_db_connection() as conn:
            user = await get_user_by_id(user_id, rds)
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
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
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def linkTelegramAccount(body, user_id, token, rds=None):
    try:
        async with get_db_connection() as conn:
            existingUser = await get_user_by_id(user_id, rds)
            if existingUser is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
            if rds:
                try:
                    await rds.delete(f"user:{user_id}")
                    if existingUser['telegram_id']:
                        await rds.delete(f"user_telegram:{existingUser['telegram_id']}")
                except Exception as e:
                    print(f"Failed to delete cache user:{user_id}: {e}")

            
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
            
            async with conn.transaction():
                user = await conn.fetchrow(update_user_query, body.telegram_id, body.telegram_username, current_time, user_id)
                await conn.execute(update_token_query, True, user_id, token)

                if rds and user:
                    try:
                        await rds.setex(f"user:{user_id}", 900, json.dumps(dict(user), default=str))
                        if user['telegram_id']:
                            await rds.setex(f"user_telegram:{user['telegram_id']}", 900, json.dumps(dict(user), default=str))
                    except Exception as e:
                        print(f"Failed to cache user:{user_id}: {e}")
                        
                return dict(user)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def validateTokenAndGetUser(token: str, rds: Redis = Depends(get_redis)):
    try:
        async with get_db_connection() as conn:
            token_query = "SELECT * FROM google_telegram_link WHERE token = $1"
            token_data = await conn.fetchrow(token_query, token)

            if token_data is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token.")
            
            if token_data['is_used']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This token has already been used.")

            if token_data['expires_at'] < pendulum.now('UTC'):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This token has expired.")

            user_id = token_data['user_id']

            user = await get_user_by_id(user_id, rds)
            return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")