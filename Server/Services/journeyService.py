from Database.connection import get_db_connection
import pendulum
from fastapi import HTTPException, status
from redis.asyncio import Redis
import json
from Models.googleCalendarModel import CalendarEvent
from Services.googleCalendarService import update_calendar_event, delete_calendar_event
from Services.userService import get_user_by_id
from Services.redisService import get_redis

async def get_existing_journeys(user_id, rds=None):
    try:
        async with get_db_connection() as conn:
            if rds:
                try:
                    cache_key = f"journeys:user:{user_id}"
                    cached_journeys = await rds.get(cache_key)
                    if cached_journeys:
                        print(f"journeys:user:{user_id} cache exists")
                        return json.loads(cached_journeys)
                except Exception as e:
                    print(f"Redis error: {e}")

            journeys_query = """
                    SELECT * FROM journeys WHERE user_id = $1
                    """
            
            journeys_records = await conn.fetch(journeys_query, user_id)

            if not journeys_records:
                return []
            
            journeys_ids = [journey['id'] for journey in journeys_records]

            custom_reminders_query = """
                    SELECT * FROM custom_reminders WHERE journey_id = ANY($1::bigint[])
                    """
            
            custom_reminders = await conn.fetch(custom_reminders_query, journeys_ids)

            reminders_map = {}
            for reminder in custom_reminders:
                if reminder['journey_id'] not in reminders_map:
                    reminders_map[reminder['journey_id']] = []
                reminders_map[reminder['journey_id']].append(dict(reminder))

            journeys = []
            for journey in journeys_records:
                journey_dict = dict(journey)
                journey_dict['custom_reminders'] = reminders_map.get(journey['id'], [])
                journeys.append(journey_dict)

            if rds and journeys:
                try:
                    await rds.setex(f"journeys:user:{user_id}", 900, json.dumps(journeys), default=str)
                    print(f"Cached journeys:user:{user_id}")
                except Exception as e:
                    print(f"Failed to cache journeys:user:{user_id}: {e}")

            return journeys
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def add_journey(body, user_id, rds=None):
    try:
        if rds:
            try:
                cached_journeys = await rds.get(f"journeys:user:{user_id}")
                if cached_journeys:
                    await rds.delete(f"journeys:user:{user_id}")
                    print(f"Cache journeys:user:{user_id} is deleted")
                else:
                    print(f"There is no cache journeys:user:{user_id} to be deleted")
            except Exception as e:
                print(f"Failed to delete cache journeys:user:{user_id}: {e}")

        journey = None
        journey_id = None
        async with get_db_connection() as conn:

            journey_query = """
                                INSERT INTO journeys
                                (user_id, journey_name, journey_date, release_day_date, day_before_release_date, reminder_on_release_day, reminder_on_day_before, sent_reminder_release_day, sent_reminder_day_before, last_updated_at)
                                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                                RETURNING id
                            """
            
            current_time = pendulum.now('UTC')
            release_day_date = pendulum.parse(body.journey_date).date().subtract(days=60)
            day_before_release_date = release_day_date.subtract(days=1)

            async with conn.transaction():
                new_journey = await conn.fetchrow(journey_query, user_id, body.journey_name, body.journey_date, release_day_date, day_before_release_date, body.remind_on_release_day, body.remind_on_day_before, False, False, current_time)

                if body.custom_dates:
                    records_to_insert = [(new_journey['id'], date, False) for date in body.custom_dates]
                    await conn.copy_records_to_table('custom_reminders', columns = ['journey_id', 'reminder_date', 'is_sent'], records = records_to_insert)

                journey_id = new_journey['id']

        journey = await get_journey_by_id(user_id, journey_id)
        return journey
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def update_journey(body, user_id, journey_id, rds=None):
    try:
        async with get_db_connection() as conn:
            if rds:
                try:
                    cached_journeys = await rds.get(f"journeys:user:{user_id}")
                    if cached_journeys:
                        await rds.delete(f"journeys:user:{user_id}")
                        print(f"Cache journeys:user:{user_id} is deleted")
                    else:
                        print(f"There is no cache journeys:user:{user_id} to be deleted")
                except Exception as e:
                    print(f"Failed to delete cache journeys:user:{user_id}: {e}")

            get_query = """
                    SELECT j.user_id, j.id as journey_id, j.journey_name, j.journey_date, j.google_calendar_event_id_release_date, j.google_calendar_event_id_day_before_release, j.release_day_date,
                    j.day_before_release_date, j.reminder_on_release_day, j.reminder_on_day_before,
                    cr.id as custom_reminder_id, cr.journey_id as custom_reminder_journey_id, cr.reminder_date, cr.google_calendar_event_id_custom_date
                    FROM journeys j LEFT JOIN custom_reminders cr
                    ON j.id = cr.journey_id
                    WHERE j.user_id = $1 AND j.id = $2
                """
            
            records = await conn.fetch(get_query, user_id, journey_id)
            if not records:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found")
            if records[0]['user_id'] != user_id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this journey")
            
            journey_name = records[0]['journey_name']

            if body.journey_name is not None:
                journey_name = body.journey_name
            
            async with conn.transaction():
                update_journey_query = """
                                        UPDATE journeys
                                        SET reminder_on_release_day = $1,
                                        reminder_on_day_before = $2,
                                        journey_name = $3
                                        WHERE id = $4
                                    """
                await conn.execute(update_journey_query, body.reminder_on_release_day, body.reminder_on_day_before, journey_name, journey_id)
                user = await get_user_by_id(user_id, rds)
                if user['calendar_enabled'] and records[0]['google_calendar_event_id_release_date']:
                    await update_calendar_event(
                        user['google_refresh_token'],
                        records[0]['google_calendar_event_id_release_date'],
                        CalendarEvent(
                            summary=f"Hi! Tatkal tickets will be release today for your journey {records[0]['journey_name']} on {records[0]['journey_date']}",
                            desc=f"Today is the tatkal tickets release day for your journey {records[0]['journey_name']} on {records[0]['journey_date']}",
                            start_time=records[0]['release_day_datelease_date'],
                            end_time=f"{pendulum.parse(records[0]['release_day_datelease_date']).add(days=1)}"
                        ))
                    
                if user['calendar_enabled'] and records[0]['google_calendar_event_id_day_before_release']:
                    await update_calendar_event(
                        user['google_refresh_token'],
                        records[0]['google_calendar_event_id_day_before_release'],
                        CalendarEvent(
                            summary=f"Hi! Tatkal tickets will be release tomorrow for your journey {records[0]['journey_name']} on {records[0]['journey_date']}",
                            desc=f"Today is the tatkal tickets release day for your journey {records[0]['journey_name']} on {records[0]['journey_date']}",
                            start_time=records[0]['day_before_release_date'],
                            end_time=f"{pendulum.parse(records[0]['day_before_release_date']).add(days=1)}"
                        ))

                existing_custom_reminders = [{"rd":record['reminder_date'], "eid":record['google_calendar_event_id_custom_date']} for record in records]
                reminders_to_be_deleted = []
                reminders_to_be_inserted = []
                calendar_event_ids_to_be_deleted = []

                for rem in existing_custom_reminders:
                    if rem['rd'] not in body.custom_reminders:
                        reminders_to_be_deleted.append(rem['rd'])
                        if rem['eid']:
                            calendar_event_ids_to_be_deleted.append(rem['eid'])
                
                for date in body.custom_reminders:
                    if date not in existing_custom_reminders:
                        reminders_to_be_inserted.append(date)
                
                if reminders_to_be_deleted:
                    query = "DELETE FROM custom_reminders WHERE journey_id = $1 AND reminder_date = ANY($2::date[])"
                    await conn.execute(query, journey_id, reminders_to_be_deleted)
                    
                    for eventId in calendar_event_ids_to_be_deleted:
                        await delete_calendar_event(user['google_refresh_token'], eventId)

                if reminders_to_be_inserted:
                    records_to_insert = [(journey_id, date, False) for date in reminders_to_be_inserted]
                    await conn.copy_records_to_table('custom_reminders', columns = ['journey_id', 'reminder_date', 'is_sent'], records = records_to_insert)

        journey = await get_journey_by_id(user_id, journey_id)
        return journey
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
async def delete_journey_by_id(user_id, journey_id, rds=None):
    try:
        async with get_db_connection() as conn:
            if rds:
                try:
                    cached_journeys = await rds.get(f"journeys:user:{user_id}")
                    if cached_journeys:
                        await rds.delete(f"journeys:user:{user_id}")
                        print(f"Cache journeys:user:{user_id} is deleted")
                    else:
                        print(f"There is no cache journeys:user:{user_id} to be deleted")
                except Exception as e:
                    print(f"Failed to delete cache journeys:user:{user_id}: {e}")

            async with conn.transaction():
                select_query = "SELECT user_id from journeys WHERE id = $1"
                journey = await conn.fetchrow(select_query, journey_id)

                if journey is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found")
                
                if journey['user_id'] != user_id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this journey")

                delete_query = "DELETE FROM journeys WHERE id = $1 and user_id = $2"

                result = await conn.execute(delete_query, journey_id, user_id)

                journey_details = await get_journey_by_id(user_id, journey_id)
                eventIds = [reminder['google_calendar_event_id_custom_date'] for reminder in journey['custom_reminders'] if reminder['google_calendar_event_id_custom_date']]

                user = await get_user_by_id(user_id, rds)

                if user['calendar_enabled'] and journey['google_calendar_event_id_release_date']:
                    await delete_calendar_event(user['google_refresh_token'], journey['google_calendar_event_id_release_date'])

                if user['calendar_enabled'] and journey['google_calendar_event_id_day_before_release']:
                    await delete_calendar_event(user['google_refresh_token'], journey['google_calendar_event_id_day_before_release'])

                for eventId in eventIds:
                    await delete_calendar_event(user['google_refresh_token'], eventId)

                
                if result == "DELETE 0":
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found or deleted already")

                journeys = await get_existing_journeys(user_id)

                if rds and journeys:
                    try:
                        await rds.setex(f"journeys:user:{user_id}", 900, json.dumps(journeys), default=str)
                        print(f"Cached journeys:user:{user_id}")
                    except Exception as e:
                        print(f"Failed to cache journeys:user:{user_id}: {e}")

                return journeys
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def get_journey_by_id(user_id, journey_id):
    try:
        async with get_db_connection() as conn:
            query = """
                    SELECT j.id as journey_id, j.journey_name, j.journey_date, j.google_calendar_event_id_release_date, j.google_calendar_event_id_day_before_release, j.release_day_date,
                    j.day_before_release_date, j.reminder_on_release_day, j.reminder_on_day_before,
                    cr.id as custom_reminder_id, cr.journey_id as custom_reminder_journey_id, cr.reminder_date, cr.is_sent, cr.google_calendar_event_id_custom_date
                    FROM journeys j LEFT JOIN custom_reminders cr
                    ON j.id = cr.journey_id
                    WHERE j.user_id = $1 AND j.id = $2
                """
            
            records = await conn.fetch(query, user_id, journey_id)
            if not records:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found")
            
            journey = {}
            custom_reminders = []

            for record in records:
                if not journey:
                    journey = {
                        "id" : record['journey_id'],
                        "journey_name" : record['journey_name'],
                        "journey_date" : record['journey_date'],
                        "google_calendar_event_id_release_date": record['google_calendar_event_id_release_date'],
                        "google_calendar_event_id_day_before_release": record['google_calendar_event_id_day_before_release'],
                        "release_day_date" : record['release_day_date'],
                        "day_before_release_date" : record['day_before_release_date'],
                        "reminder_on_release_day" : record['reminder_on_release_day'],
                        "reminder_on_day_before" : record['reminder_on_day_before'],
                        "custom_reminders" : []
                    }

                if record['custom_reminder_id'] is not None:
                    custom_reminders.append({
                        "id" : record['custom_reminder_id'],
                        "journey_id" : record['custom_reminder_journey_id'],
                        "reminder_date" : record['reminder_date'],
                        "is_sent" : record['is_sent'],
                        "google_calendar_event_id_custom_date": record['google_calendar_event_id_custom_date']
                    })

            journey['custom_reminders'] = custom_reminders
            return journey
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")