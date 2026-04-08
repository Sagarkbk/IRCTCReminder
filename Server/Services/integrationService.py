from Database.connection import get_db_connection
from Services.userService import get_user_by_id
import pendulum
import secrets
from fastapi import HTTPException, status, Depends
from redis.asyncio import Redis
import json
from Services.googleCalendarService import delete_calendar_event
import asyncio

async def generateLinkingToken(user_id, rds=None):
    try:
        async with get_db_connection() as conn:            
            current_time = pendulum.now('UTC')

            existing_token_query = """
                                SELECT token FROM google_telegram_link 
                                WHERE user_id = $1 AND
                                expires_at > $2 AND
                                is_used = $3
                                """
            existing_token = await conn.fetchrow(existing_token_query, user_id, current_time, False)

            if existing_token:
                return existing_token['token']
            
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
    except Exception as e:
        print(f"Error in generateLinkingToken: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def linkTelegramAccount(user_id, telegram_id, telegram_username, token, rds=None):
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
                    telegram_enabled = $3,
                    telegram_linked_at = $4,
                    last_updated_at = $4
                    WHERE id = $5
                    RETURNING *
                    """
            update_token_query = """
                                UPDATE google_telegram_link SET is_used = $1
                                WHERE user_id = $2 AND token = $3
                                """
            current_time = pendulum.now('UTC')
            
            async with conn.transaction():
                user = await conn.fetchrow(update_user_query, telegram_id, telegram_username, True, current_time, user_id)
                await conn.execute(update_token_query, True, user_id, token)

            if rds and user:
                    try:
                        await rds.delete(f"user:{user_id}")
                        if existingUser['telegram_id']:
                            await rds.delete(f"user_telegram:{existingUser['telegram_id']}")
                        await rds.setex(f"user:{user_id}", 900, json.dumps(dict(user), default=str))
                        if user['telegram_id']:
                            await rds.setex(f"user_telegram:{user['telegram_id']}", 900, json.dumps(dict(user), default=str))
                    except Exception as e:
                        print(f"Failed to cache user:{user_id}: {e}")
                        
            return dict(user)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in linkTelegramAccount: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def validateTokenAndGetUser(token: str, rds = None):
    try:
        async with get_db_connection() as conn:
            token_query = "SELECT * FROM google_telegram_link WHERE token = $1"
            token_data = await conn.fetchrow(token_query, token)

            if token_data is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token.")
            
            if token_data['is_used']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your token has already been used.")

            if token_data['expires_at'] < pendulum.now('UTC'):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This token has expired.")

            user_id = token_data['user_id']

            user = await get_user_by_id(user_id, rds)
            return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in validateTokenAndGetUser: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def revoke_all_calendar_events(user_id, rds = None):
    try:
        async with get_db_connection() as conn:
            query = """
                    SELECT u.google_refresh_token,
                    j.google_calendar_event_id_release_date, j.google_calendar_event_id_day_before_release, 
                    cr.google_calendar_event_id_custom_date 
                    FROM users u
                    LEFT JOIN journeys j ON u.id = j.user_id
                    LEFT OUTER JOIN custom_reminders cr ON j.id = cr.journey_id
                    WHERE u.id = $1
                    """
            journeys = await conn.fetch(query, user_id)

            if not journeys:
                return
            
            refresh_token = journeys[0]['google_refresh_token']

            event_ids = set()

            for journey in journeys:
                if journey['google_calendar_event_id_release_date']:
                    event_ids.add(journey['google_calendar_event_id_release_date'])
                if journey['google_calendar_event_id_day_before_release']:
                    event_ids.add(journey['google_calendar_event_id_day_before_release'])
                if journey['google_calendar_event_id_custom_date']:
                    event_ids.add(journey['google_calendar_event_id_custom_date'])
            
            async with conn.transaction():
                await conn.execute("UPDATE journeys SET google_calendar_event_id_release_date = NULL, google_calendar_event_id_day_before_release = NULL WHERE user_id = $1", user_id)
                await conn.execute("UPDATE custom_reminders SET google_calendar_event_id_custom_date = NULL WHERE journey_id IN (SELECT id FROM journeys WHERE user_id = $1)", user_id)

            if event_ids and refresh_token:
                tasks = [delete_calendar_event(refresh_token, event_id) for event_id in event_ids]
                await asyncio.gather(*tasks, return_exceptions=True)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in revoke_all_calendar_events: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")