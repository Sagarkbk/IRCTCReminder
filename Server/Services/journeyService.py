from Database.connection import get_db_connection
import pendulum
from fastapi import HTTPException, status

async def get_existing_journeys(user_id):
    try:
        async with get_db_connection() as conn:

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

            return journeys
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def add_journey(body, user_id):
    try:
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
    except Exception as e:
        raise

async def update_journey(body, user_id, journey_id):
    try:
        async with get_db_connection() as conn:
            get_query = """
                    SELECT j.id as journey_id, j.journey_name, j.release_day_date,
                    j.day_before_release_date, j.reminder_on_release_day, j.reminder_on_day_before,
                    cr.id as custom_reminder_id, cr.journey_id as custom_reminder_journey_id, cr.reminder_date
                    FROM journeys j LEFT JOIN custom_reminders cr
                    ON j.id = cr.journey_id
                    WHERE j.user_id = $1 AND j.id = $2
                """
            
            records = await conn.fetch(get_query, user_id, journey_id)
            if not records:
                return None        
            
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

                existing_custom_reminders = [record['reminder_date'] for record in records]
                reminders_to_be_deleted = []
                reminders_to_be_inserted = []

                for date in existing_custom_reminders:
                    if date not in body.custom_reminders:
                        reminders_to_be_deleted.append(date)
                
                for date in body.custom_reminders:
                    if date not in existing_custom_reminders:
                        reminders_to_be_inserted.append(date)
                
                if reminders_to_be_deleted:
                    query = "DELETE FROM custom_reminders WHERE journey_id = $1 AND reminder_date = ANY($2::date[])"
                    await conn.execute(query, journey_id, reminders_to_be_deleted)

                if reminders_to_be_inserted:
                    records_to_insert = [(journey_id, date, False) for date in reminders_to_be_inserted]
                    await conn.copy_records_to_table('custom_reminders', columns = ['journey_id', 'reminder_date', 'is_sent'], records = records_to_insert)

        journey = await get_journey_by_id(user_id, journey_id)
        return journey

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def get_journey_by_id(user_id, journey_id):
    try:
        async with get_db_connection() as conn:
            query = """
                    SELECT j.id as journey_id, j.journey_name, j.journey_date, j.release_day_date,
                    j.day_before_release_date, j.reminder_on_release_day, j.reminder_on_day_before,
                    cr.id as custom_reminder_id, cr.journey_id as custom_reminder_journey_id, cr.reminder_date, cr.is_sent
                    FROM journeys j LEFT JOIN custom_reminders cr
                    ON j.id = cr.journey_id
                    WHERE j.user_id = $1 AND j.id = $2
                """
            
            records = await conn.fetch(query, user_id, journey_id)
            if not records:
                return None
            
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

                if record['custom_reminder_id'] is not None:
                    custom_reminders.append({
                        "id" : record['custom_reminder_id'],
                        "journey_id" : record['custom_reminder_journey_id'],
                        "reminder_date" : record['reminder_date'],
                        "is_sent" : record['is_sent']
                    })

            journey['custom_reminders'] = custom_reminders
            return journey
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def delete_journey_by_id(user_id, journey_id):
    try:
        async with get_db_connection() as conn:
            async with conn.transaction():
                select_query = "SELECT user_id from journeys WHERE id = $1"
                journey = await conn.fetchrow(select_query, journey_id)

                if not journey:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found")
                
                if journey['user_id'] != user_id:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this journey")

                delete_query = "DELETE FROM journeys WHERE id = $1 and user_id = $2"

                result = await conn.execute(delete_query, journey_id, user_id)

                if result == "DELETE 0":
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journey not found or deleted already")

                journeys = await get_existing_journeys(user_id)
                return journeys
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)