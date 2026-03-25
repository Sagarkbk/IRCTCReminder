from Database.connection import get_db_connection
import pendulum
from fastapi import HTTPException, status, Depends
import json
from redis.asyncio import Redis

async def create_user(userInfo, google_refresh_token, rds=None):
    try:
        async with get_db_connection() as conn:
            query = """
                    INSERT INTO users (google_id, email, username, google_refresh_token, calendar_enabled, last_updated_at) 
                    VALUES ($1, $2, $3, $4, $5, $6) 
                    RETURNING id, email, username, calendar_enabled, telegram_enabled, telegram_id
                    """
            result = await conn.fetchrow(
                                        query, 
                                        userInfo.get('sub'), 
                                        userInfo.get('email'), 
                                        userInfo.get('name'),
                                        google_refresh_token,
                                        True,
                                        pendulum.now('UTC')
                                    )
            
            if rds and result:
                try:
                    await rds.setex(f"user:{result['id']}", 900, json.dumps(dict(result), default=str))
                except Exception as e:
                    print(f"Failed to cache user:{result['id']}: {e}")

            return dict(result)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def get_user_by_id(user_id, rds=None):
    try:
        if rds:
            try:
                cache_key = f"user:{user_id}"
                cached_user = await rds.get(cache_key)
                if cached_user:
                    print(f"user:{user_id} cache exists")
                    return json.loads(cached_user)
            except Exception as e:
                print(f"Redis error: {e}")
            

        async with get_db_connection() as conn:
            query = """
                    SELECT id, email, username, google_refresh_token, calendar_enabled, telegram_enabled, telegram_id FROM users WHERE id = $1
                    """
            existingUser = await conn.fetchrow(query, user_id)
            if existingUser is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            if rds and existingUser:
                try:
                    await rds.setex(f"user:{user_id}", 900, json.dumps(dict(existingUser), default=str))
                except Exception as e:
                    print(f"Failed to cache user:{user_id}: {e}")

            return dict(existingUser)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def get_user_by_google_id(google_id):
    try:
        async with get_db_connection() as conn:
            query = """
                    SELECT id, email, username, calendar_enabled, telegram_enabled, telegram_id FROM users WHERE google_id = $1
                    """
            existingUser = await conn.fetchrow(query, google_id)
            if existingUser is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            return dict(existingUser)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def update_user(userInfo, user_id, google_refresh_token, rds=None):
    try:
        async with get_db_connection() as conn:
            query = """
                    UPDATE users 
                    SET email = $1, username = $2, 
                    google_refresh_token = COALESCE($3, google_refresh_token), 
                    last_updated_at = $4
                    WHERE id = $5
                    RETURNING id, email, username, google_refresh_token, calendar_enabled, telegram_enabled, telegram_id
                    """
            if rds:
                try:
                    cached_user_str = await rds.get(f"user:{user_id}")
                    if cached_user_str:
                        cached_user = json.loads(cached_user_str)
                        await rds.delete(f"user:{user_id}")
                        print(f"Deleted cache user:{user_id}")
                        if cached_user and cached_user.get('telegram_id'):
                            cached_telegram = await rds.get(f"user_telegram:{cached_user.get('telegram_id')}")
                            if cached_telegram:
                                await rds.delete(f"user_telegram:{cached_user.get('telegram_id')}")
                                print(f"Deleted cache user_telegram:{cached_user.get('telegram_id')}")
                            else:
                                print(f"There is no cache user_telegram:{cached_user.get('telegram_id')} to be deleted")
                    else:
                        print(f"There is no cache user:{user_id} to be deleted")
                except Exception as e:
                    print(f"Failed to delete cache user:{user_id}: {e}")

            result = await conn.fetchrow(
                                        query, 
                                        userInfo.get('email'),
                                        userInfo.get('name'),
                                        google_refresh_token,
                                        pendulum.now('UTC'),
                                        user_id
                                    )
            
            try:
                await rds.setex(f"user:{user_id}", 900, json.dumps(dict(result), default=str))
                if result['telegram_id']:
                    await rds.setex(f"user_telegram:{result['telegram_id']}", 900, json.dumps(dict(result), default=str))
            except Exception as e:
                print(f"Failed to cache user:{user_id}: {e}")
            
            return dict(result)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
async def update_user_settings(user_id, body, rds = None):
    try:
        async with get_db_connection() as conn:
            user = await get_user_by_id(user_id, rds)
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
            if rds:
                try:
                    cached_user = await rds.get(f"user:{user_id}")
                    if cached_user:
                        await rds.delete(f"user:{user_id}")
                        if user.get('telegram_id'):
                            cached_telegram = await rds.get(f"user_telegram:{user['telegram_id']}")
                            if cached_telegram:
                                await rds.delete(f"user_telegram:{user['telegram_id']}")
                    else:
                        print(f"There is no cache user:{user_id} to be deleted")
                except Exception as e:
                    print(f"Failed to delete cache user:{user_id}: {e}")

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
                    RETURNING id, email, username, google_refresh_token, calendar_enabled, telegram_enabled, telegram_id
                    """
            updated_user = await conn.fetchrow(query, calendar_enabled, telegram_enabled,
                                            pendulum.now('UTC'), user_id)
            
            if user['calendar_enabled'] and not updated_user['calendar_enabled']:
                from Services.integrationService import revoke_all_calendar_events
                await revoke_all_calendar_events(user_id, rds)
            
            if rds and updated_user:
                try:
                    await rds.setex(f"user:{user_id}", 900, json.dumps(dict(updated_user), default=str))
                    if updated_user['telegram_id']:
                        await rds.setex(f"user_telegram:{updated_user['telegram_id']}", 900, json.dumps(dict(updated_user), default=str))
                except Exception as e:
                    print(f"Failed to cache user:{user_id}: {e}")

            return dict(updated_user)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
async def get_user_by_telegram_id(telegram_id, rds=None):
    try:
        if rds:
            try:
                cache_key = f"user_telegram:{telegram_id}"
                cached_user = await rds.get(cache_key)
                if cached_user:
                    print(f"user_telegram:{telegram_id} cache exists")
                    return json.loads(cached_user)
            except Exception as e:
                print(f"Redis error: {e}")
            

        async with get_db_connection() as conn:
            query = """
                    SELECT * FROM users WHERE telegram_id = $1
                    """
            existingUser = await conn.fetchrow(query, telegram_id)
            if existingUser is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            if rds and existingUser:
                try:
                    await rds.setex(f"user_telegram:{telegram_id}", 900, json.dumps(dict(existingUser), default=str))
                except Exception as e:
                    print(f"Failed to cache user_telegram:{telegram_id}: {e}")

            return dict(existingUser)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")