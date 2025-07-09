from Database.connection import get_db_connection
from datetime import datetime, timezone

async def get_existing_holidays(user_id):
    try:
        conn = await get_db_connection()
        query = """
                SELECT * FROM selected_holidays WHERE user_id = $1
                """
        holidays = await conn.fetch(query, user_id)
        return holidays
    except Exception as e:
        raise

async def add_holidays(body):
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
        for hn, hd, cat, dbs, rds in zip(body['holiday_name'], body['holiday_date'], 
                                        body['category'], body['day_before_sent'], 
                                        body['release_day_sent']):
            holiday = await conn.execute(query, body['user_id'], hn, hd, cat, dbs, rds, current_time)
            holidays.append(holiday)
        return holidays
    except Exception as e:
        raise

async def update_holidays(body):
    try:
        conn = await get_db_connection()
        check_if_exists = """
                SELECT * FROM selected_holidays WHERE user_id = $1 AND holiday_name = $2 AND holiday_date = $3
                """
        update_holiday = """
                UPDATE selected_holidays SET day_before_sent = $1, release_day_sent = $2, last_updated_at = $3
                WHERE user_id = $4 AND holiday_name = $5 AND holiday_date = $6 AND category = $7
                RETURNING *
                """
        add_holiday = """
                INSERT INTO selected_holidays
                (user_id, holiday_name, holiday_date, category, day_before_sent, release_day_sent, last_updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *
                """
        current_time = datetime.now(timezone.utc)
        holidays = []
        for hn, hd, cat, dbs, rds in zip(body['holiday_name'], body['holiday_date'], 
                                        body['category'], body['day_before_sent'], 
                                        body['release_day_sent']):
            exists = await conn.fetch(check_if_exists, body.user_id, hn, hd)
            if exists:
                holiday = await conn.execute(
                                            update_holiday,
                                            dbs,
                                            rds,
                                            current_time,
                                            body.user_id,
                                            hn,
                                            hd,
                                            cat
                                        )
                holidays.append(holiday)
            else:
                holiday = await conn.execute(
                                            add_holiday,
                                            body.user_id,
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
        raise