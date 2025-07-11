from Database.connection import get_db_connection
from datetime import datetime, timezone
from fastapi import HTTPException, status

async def get_existing_holidays(user_id):
    try:
        conn = await get_db_connection()
        query = """
                SELECT * FROM selected_holidays WHERE user_id = $1
                """
        holidays = await conn.fetch(query, user_id)
        return holidays
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

async def add_holidays(body, user_id):
    try:
        conn = await get_db_connection()
        query = """
                INSERT INTO selected_holidays
                (user_id, holiday_name, holiday_date, category, day_before_sent, release_day_sent, last_updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *
                """
        current_time = datetime.now(timezone.utc)
        holidays = []
        for hn, hd, cat, dbs, rds in zip(body.holiday_name, body.holiday_date, 
                                            body.category, body.day_before_sent, 
                                            body.release_day_sent):
            holiday = await conn.fetchrow(query, user_id, hn, hd, cat, dbs, rds, current_time)
            holidays.append(holiday)
        return holidays
    except Exception as e:
        raise

async def update_holidays(body, user_id):
    try:
        conn = await get_db_connection()
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
                RETURNING *
                """
        current_time = datetime.now(timezone.utc)
        holidays = []
        async with await conn.transaction() as trsc:
            for hn, hd, cat, dbs, rds in zip(body.holiday_name, body.holiday_date, 
                                            body.category, body.day_before_sent, 
                                            body.release_day_sent):
                holiday = await trsc.fetchrow(
                                            upsert_holiday,
                                            user_id,
                                            hn,
                                            hd,
                                            cat,
                                            dbs,
                                            rds,
                                            current_time
                                        )
                holidays.append(holiday)
        return holidays
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)