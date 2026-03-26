from Database.connection import get_db_connection
import pendulum
from fastapi import HTTPException, status
from redis.asyncio import Redis
import json
from Models.googleCalendarModel import CalendarEvent
from Services.googleCalendarService import update_calendar_event, delete_calendar_event
from Services.userService import get_user_by_id
import asyncio
from datetime import datetime

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
                    SELECT id, journey_name, journey_date, release_day_date, day_before_release_date, reminder_on_release_day, reminder_on_day_before FROM journeys WHERE user_id = $1
                    """
            
            journeys_records = await conn.fetch(journeys_query, user_id)

            if not journeys_records:
                return []
            
            journeys_ids = [journey['id'] for journey in journeys_records]

            custom_reminders_query = """
                    SELECT journey_id, reminder_date FROM custom_reminders WHERE journey_id = ANY($1::bigint[])
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
                    await rds.setex(f"journeys:user:{user_id}", 900, json.dumps(journeys, default=str))
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
            async with conn.transaction():

                journey_query = """
                                    INSERT INTO journeys
                                    (user_id, journey_name, journey_date, release_day_date, day_before_release_date, reminder_on_release_day, reminder_on_day_before, last_updated_at)
                                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                                    RETURNING id
                                """
                
                current_time = pendulum.now('UTC')
                release_day_date = pendulum.parse(str(body.journey_date)).subtract(days=60)
                day_before_release_date = release_day_date.subtract(days=1)
                print(body)

                new_journey = await conn.fetchrow(journey_query, user_id, body.journey_name, body.journey_date, release_day_date, day_before_release_date, body.reminder_on_release_day, body.reminder_on_day_before, current_time)

                if body.custom_reminders:
                    records_to_insert = [(new_journey['id'], date) for date in body.custom_reminders]
                    await conn.copy_records_to_table('custom_reminders', columns = ['journey_id', 'reminder_date'], records = records_to_insert)

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

            name_changed = False
   
            if body.journey_name is not None and body.journey_name != records[0]['journey_name']:
                journey_name = body.journey_name
                name_changed = True                
            
            async with conn.transaction():
                update_journey_query = """
                                        UPDATE journeys
                                        SET reminder_on_release_day = $1,
                                        reminder_on_day_before = $2,
                                        journey_name = $3,
                                        google_calendar_event_id_release_date = CASE WHEN $1 = FALSE THEN NULL ELSE google_calendar_event_id_release_date END,
                                        google_calendar_event_id_day_before_release = CASE WHEN $2 = FALSE THEN NULL ELSE google_calendar_event_id_day_before_release END
                                        WHERE id = $4
                                    """
                await conn.execute(update_journey_query, body.reminder_on_release_day, body.reminder_on_day_before, journey_name, journey_id)
                user = await get_user_by_id(user_id, rds)
                if user['calendar_enabled'] and records[0]['google_calendar_event_id_release_date']:
                    if not body.reminder_on_release_day:
                        await delete_calendar_event(user['google_refresh_token'],
                        records[0]['google_calendar_event_id_release_date'])
                    elif name_changed:
                        await update_calendar_event(
                        user['google_refresh_token'],
                        records[0]['google_calendar_event_id_release_date'],
                        CalendarEvent(
                            summary=f"Hi! Tatkal tickets will be release today for your journey {journey_name} on {records[0]['journey_date']}",
                            desc=f"Today is the tatkal tickets release day for your journey {journey_name} on {records[0]['journey_date']}",
                            start_time=pendulum.instance(datetime.combine(records[0]['release_day_date'], datetime.min.time())).at(8, 0, 0),
                            end_time=pendulum.instance(datetime.combine(records[0]['release_day_date'], datetime.min.time())).at(9, 0, 0),
                            reminders={
                                        "useDefault": False,
                                        "overrides": [
                                            {"method": "popup", "minutes": 60},
                                            {"method": "popup", "minutes": 10},
                                            {"method": "popup", "minutes": 0},
                                        ]
                                    }
                        ))
                    
                if user['calendar_enabled'] and records[0]['google_calendar_event_id_day_before_release']:
                    if not body.reminder_on_day_before:
                        await delete_calendar_event(user['google_refresh_token'],
                        records[0]['google_calendar_event_id_day_before_release'])
                    elif name_changed:
                        await update_calendar_event(
                            user['google_refresh_token'],
                            records[0]['google_calendar_event_id_day_before_release'],
                            CalendarEvent(
                                summary=f"Hi! Tatkal tickets will be release tomorrow for your journey {journey_name} on {records[0]['journey_date']}",
                                desc=f"Tomorrow is the tatkal tickets release day for your journey {journey_name} on {records[0]['journey_date']}",
                                start_time=pendulum.instance(datetime.combine(records[0]['day_before_release_date'], datetime.min.time())).at(8, 0, 0),
                                end_time=pendulum.instance(datetime.combine(records[0]['day_before_release_date'], datetime.min.time())).at(9, 0, 0),
                                reminders={
                                            "useDefault": False,
                                            "overrides": [
                                                {"method": "popup", "minutes": 60},
                                                {"method": "popup", "minutes": 10},
                                                {"method": "popup", "minutes": 0},
                                            ]
                                        }
                            ))
                
                existing_custom_reminders = [{"rd":record['reminder_date'], "eid":record['google_calendar_event_id_custom_date']} for record in records]

                existing_custom_reminders_dates = {rem['rd'] for rem in existing_custom_reminders if rem['rd']}
                
                reminders_to_be_deleted = []
                reminders_to_be_inserted = []
                calendar_event_ids_to_be_deleted = []
    
                for rem in existing_custom_reminders:
                    if rem['rd'] and rem['rd'] not in body.custom_reminders:
                        reminders_to_be_deleted.append(rem['rd'])
                        if rem['eid']:
                            calendar_event_ids_to_be_deleted.append(rem['eid'])
                    
                for date in body.custom_reminders:
                    if date not in existing_custom_reminders_dates:
                        reminders_to_be_inserted.append(date)
                
                if reminders_to_be_deleted:
                    query = "DELETE FROM custom_reminders WHERE journey_id = $1 AND reminder_date = ANY($2::date[])"
                    await conn.execute(query, journey_id, reminders_to_be_deleted)
                    
                    for eventId in calendar_event_ids_to_be_deleted:
                        await delete_calendar_event(user['google_refresh_token'], eventId)

                if reminders_to_be_inserted:
                    records_to_insert = [(journey_id, date) for date in reminders_to_be_inserted]
                    await conn.copy_records_to_table('custom_reminders', columns = ['journey_id', 'reminder_date'], records = records_to_insert)
                
                if name_changed:
                    for rem in existing_custom_reminders:
                        if rem['rd'] and rem['rd'] in body.custom_reminders and rem['eid']:
                            await update_calendar_event(
                                    user['google_refresh_token'],
                                    rem['eid'],
                                    CalendarEvent(
                                        summary=f"IRCTC Tickets Booking for {journey_name} on {records[0]['journey_date']}",
                                        desc=f"Hii! This is your custom reminder for booking train tickets for your {journey_name} on {records[0]['journey_date']}",
                                        start_time=pendulum.instance(datetime.combine(rem['rd'], datetime.min.time())).at(8, 0, 0),
                                        end_time=pendulum.instance(datetime.combine(rem['rd'], datetime.min.time())).at(9, 0, 0),
                                        reminders={
                                            "useDefault": False,
                                            "overrides": [
                                                {"method": "popup", "minutes": 60},
                                                {"method": "popup", "minutes": 10},
                                                {"method": "popup", "minutes": 0},
                                            ]
                                        }
                                    )
                                )

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
            
            query = """
                    SELECT j.user_id, j.google_calendar_event_id_release_date, 
                    j.google_calendar_event_id_day_before_release,
                    cr.google_calendar_event_id_custom_date
                    FROM journeys j
                    LEFT JOIN custom_reminders cr ON j.id = cr.journey_id
                    WHERE j.id = $1
                    """
            
            journeys = await conn.fetch(query, journey_id)

            if not journeys:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found")
            
            if journeys[0]['user_id'] != user_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
            
            event_ids = set()

            for journey in journeys:
                if journey['google_calendar_event_id_release_date']:
                    event_ids.add(journey['google_calendar_event_id_release_date'])
                if journey['google_calendar_event_id_day_before_release']:
                    event_ids.add(journey['google_calendar_event_id_day_before_release'])
                if journey['google_calendar_event_id_custom_date']:
                    event_ids.add(journey['google_calendar_event_id_custom_date'])
            
            async with conn.transaction():
                await conn.execute("DELETE FROM journeys WHERE id = $1 AND user_id = $2", journey_id, user_id)

            user = await get_user_by_id(user_id, rds)
            if event_ids:
                tasks = [delete_calendar_event(user['google_refresh_token'], eventId) for eventId in event_ids]
                await asyncio.gather(*tasks, return_exceptions=True)

            return "Journey deleted successfully"
            
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def get_journey_by_id(user_id, journey_id):
    try:
        async with get_db_connection() as conn:
            query = """
                    SELECT j.id as journey_id, j.journey_name, j.journey_date, j.release_day_date,
                    j.day_before_release_date, j.reminder_on_release_day, j.reminder_on_day_before,
                    cr.journey_id as custom_reminder_journey_id, cr.reminder_date
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
                        "release_day_date" : record['release_day_date'],
                        "day_before_release_date" : record['day_before_release_date'],
                        "reminder_on_release_day" : record['reminder_on_release_day'],
                        "reminder_on_day_before" : record['reminder_on_day_before'],
                        "custom_reminders" : []
                    }

                if record['reminder_date'] is not None:
                    custom_reminders.append({
                        "journey_id" : record['custom_reminder_journey_id'],
                        "reminder_date" : record['reminder_date'],
                    })

            journey['custom_reminders'] = custom_reminders
            return journey
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
async def get_journey_stats(user_id):
    try:
        async with get_db_connection() as conn:
            query = """
                    SELECT COUNT(*) AS total_journeys, 
                    COUNT(*) FILTER (WHERE journey_date < $1) AS completed_journeys, 
                    COUNT(*) FILTER (WHERE journey_date >= $1) AS yet_to_complete_journeys
                    FROM journeys 
                    WHERE user_id = $2;
                    """
            today = pendulum.now('Asia/Kolkata').date()
            stats = await conn.fetchrow(query, today, user_id)
            return dict(stats)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")