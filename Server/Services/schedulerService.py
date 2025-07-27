from fastapi import HTTPException, status
from Telegram_Bot.bot import send_message
from Services.googleCalendarService import create_calendar_event
from Database.connection import get_db_connection
import pendulum
from Models.googleCalendarModel import CalendarEvent

async def send_reminders():
    try:
        conn = await get_db_connection()

        today = pendulum.now('UTC').date()

        get_release_day_reminders = """"
                                    SELECT u.id as uid, u.google_refresh_token, u.telegram_id, u.calendar_enabled, u.telegram_enabled, j.* 
                                    FROM users u JOIN journeys j
                                    ON u.id = j.user_id
                                    WHERE j.release_day_date = $1
                                    """
        release_day_reminders = await conn.fetch(get_release_day_reminders, today)

        for reminder in release_day_reminders:
            if reminder['calendar_enabled'] and not reminder['google_calendar_event_id_release_date']:
                details = CalendarEvent(
                                    summary=f"IRCTC Tickets Booking for {reminder['journey_name']} on {reminder['journey_date']}",
                                    desc=f"Hii! This is your reminder that tickets for your {reminder['journey_name']} on {reminder['journey_date']} will be released today at 8AM IST",
                                    start_time=reminder['release_day_date'],
                                    end_time=pendulum.parse(reminder['release_day_date']).add(hours=23))
                eventId = await create_calendar_event(reminder['google_refresh_token'], details)

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server issue")