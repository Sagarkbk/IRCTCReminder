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

async def add_journeys(body, user_id):
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
            remind_on_release_day = False
            remind_on_day_before = False
            custom_dates = []

            for reminder_date in body.reminder_dates:
                reminder_date = pendulum.parse(reminder_date).date()
                if reminder_date == release_day_date:
                    remind_on_release_day = True
                elif reminder_date == day_before_release_date:
                    remind_on_day_before = True
                else:
                    custom_dates.append(reminder_date)

            async with conn.transaction():
                new_journey = await conn.fetchrow(journey_query, user_id, body.journey_name, body.journey_date, release_day_date, day_before_release_date, remind_on_release_day, remind_on_day_before, False, False, current_time)

                records_to_insert = [(new_journey['id'], date, False) for date in custom_dates]
                await conn.copy_records_to_table('custom_reminders', columns = ['journey_id', 'reminder_date', 'is_sent'], records = records_to_insert)

                journey_id = new_journey['id']

        journey = await get_journey_by_id(journey_id)
        return journey
    except Exception as e:
        raise

async def update_journeys(body, user_id):
    try:
        async with get_db_connection() as conn:

            upsert_holiday = """
                    INSERT INTO selected_holidays
                    (user_id, holiday_name, holiday_date, category, day_before_sent, release_day_sent, last_updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    ON CONFLICT (user_id, holiday_name, holiday_date)
                    DO UPDATE
                    SET category = EXCLUDED.category,
                    day_before_sent = EXCLUDED.day_before_sent,
                    release_day_sent = EXCLUDED.release_day_sent,
                    last_updated_at = EXCLUDED.last_updated_at
                """
            
            current_time = pendulum.now('UTC')

            async with conn.transaction():

                for hn, hd, cat, dbs, rds in zip(body.holiday_name, body.holiday_date, 
                                                body.category, body.day_before_sent, 
                                                body.release_day_sent):
                    await conn.execute(
                                                upsert_holiday,
                                                user_id,
                                                hn,
                                                hd,
                                                cat,
                                                dbs,
                                                rds,
                                                current_time
                                            )
                    
            holidays = await get_existing_journeys(user_id)
            return holidays
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def get_journey_by_id(journey_id):
    try:
        async with get_db_connection() as conn:
            query = """
                    SELECT j.id as journey_id, j.journey_name, j.journey_date, j.release_day_date,
                    j.day_before_release_date, j.reminder_on_release_day, j.reminder_on_day_before,
                    cr.id as custom_reminder_id, cr.journey_id as custom_reminder_journey_id, cr.reminder_date, cr.is_sent
                    FROM journeys j LEFT JOIN custom_reminders cr
                    ON j.id = cr.journey_id
                    WHERE j.id = $1
                """
            
            records = await conn.fetch(query, journey_id)
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