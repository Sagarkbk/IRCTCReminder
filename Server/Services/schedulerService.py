from Telegram_Bot.bot import send_message
from Services.googleCalendarService import create_calendar_event
from Database.connection import get_db_connection
import pendulum
from Models.googleCalendarModel import CalendarEvent

async def create_google_calendar_event():
    try:
        async with get_db_connection() as conn:
            
            get_all_standard_reminders = """
                                        SELECT u.id as uid, u.google_refresh_token, u.telegram_id, u.calendar_enabled, u.telegram_enabled, j.* 
                                        FROM users u 
                                        JOIN journeys j ON u.id = j.user_id
                                        WHERE u.calendar_enabled = TRUE AND (j.reminder_on_release_day = TRUE OR j.reminder_on_day_before = TRUE)
                                        """
            
            standard_reminders = await conn.fetch(get_all_standard_reminders)
            
            for reminder in standard_reminders:
                try:
                    if reminder['reminder_on_release_day'] and not reminder['google_calendar_event_id_release_date']:
                        date = reminder['release_day_date']
                        event_day_ist = pendulum.datetime(date.year, date.month, date.day, tz='Asia/Kolkata')
                        event_start_time = event_day_ist.add(hours=8)
                        event_end_time = event_day_ist.add(hours=9)
                        details = CalendarEvent(
                                            summary=f"IRCTC Tickets Booking for {reminder['journey_name']} on {reminder['journey_date']}",
                                            desc=f"Hii! This is your reminder that tickets for your {reminder['journey_name']} on {reminder['journey_date']} will be released today at 8AM IST",
                                            start_time=event_start_time,
                                            end_time=event_end_time,
                                            reminders={
                                                "useDefault": False,
                                                "overrides": [
                                                    {"method": "popup", "minutes": 60},
                                                    {"method": "popup", "minutes": 10},
                                                    {"method": "popup", "minutes": 0},
                                                ]
                                            }
                                        )
                        eventId = await create_calendar_event(reminder['google_refresh_token'], details)
                        await conn.execute(
                                        "UPDATE journeys SET google_calendar_event_id_release_date=$1 WHERE user_id=$2 AND id=$3", 
                                        eventId, 
                                        reminder['uid'], 
                                        reminder['id'] 
                                    )
                    
                    if reminder['reminder_on_day_before'] and not reminder['google_calendar_event_id_day_before_release']:
                        date = reminder['day_before_release_date']
                        event_day_ist = pendulum.datetime(date.year, date.month, date.day, tz='Asia/Kolkata')
                        event_start_time = event_day_ist.add(hours=8)
                        event_end_time = event_day_ist.add(hours=9)
                        details = CalendarEvent(
                                            summary=f"IRCTC Tickets Booking for {reminder['journey_name']} on {reminder['journey_date']}",
                                            desc=f"Hii! This is your reminder that tickets for your {reminder['journey_name']} on {reminder['journey_date']} will be released tomorrow at 8AM IST",
                                            start_time=event_start_time,
                                            end_time=event_end_time,
                                            reminders={
                                                "useDefault": False,
                                                "overrides": [
                                                    {"method": "popup", "minutes": 60},
                                                    {"method": "popup", "minutes": 10},
                                                    {"method": "popup", "minutes": 0},
                                                ]
                                            }
                                        )
                        eventId = await create_calendar_event(reminder['google_refresh_token'], details)
                        await conn.execute(
                                        "UPDATE journeys SET google_calendar_event_id_day_before_release=$1 WHERE user_id=$2 AND id=$3", 
                                        eventId, 
                                        reminder['uid'], 
                                        reminder['id'] 
                                    )
        
                except Exception as e:
                    continue
            
            get_all_custom_reminders = """
                                        SELECT u.google_refresh_token, j.journey_name, j.journey_date, cr.*
                                        FROM users u
                                        JOIN journeys j ON u.id = j.user_id 
                                        JOIN custom_reminders cr ON j.id = cr.journey_id 
                                        WHERE u.calendar_enabled = TRUE 
                                        AND cr.google_calendar_event_id_custom_date IS NULL
                                        """
            
            custom_reminders = await conn.fetch(get_all_custom_reminders)

            for reminder in custom_reminders:
                try:
                    date = reminder['reminder_date']
                    event_day_ist = pendulum.datetime(date.year, date.month, date.day, tz='Asia/Kolkata')
                    event_start_time = event_day_ist.add(hours=8)
                    event_end_time = event_day_ist.add(hours=9)
                    details = CalendarEvent(
                                        summary=f"IRCTC Tickets Booking for {reminder['journey_name']} on {reminder['journey_date']}",
                                        desc=f"Hii! This is your custom reminder for booking train tickets for your {reminder['journey_name']} on {reminder['journey_date']}",
                                        start_time=event_start_time,
                                        end_time=event_end_time,
                                        reminders={
                                            "useDefault": False,
                                            "overrides": [
                                                {"method": "popup", "minutes": 60},
                                                {"method": "popup", "minutes": 10},
                                                {"method": "popup", "minutes": 0},
                                            ]
                                        }
                                    )
                    eventId = await create_calendar_event(reminder['google_refresh_token'], details)
                    await conn.execute(
                                    "UPDATE custom_reminders SET google_calendar_event_id_custom_date=$1 WHERE id=$2", 
                                    eventId, 
                                    reminder['id'] 
                                )
                except Exception as e:
                    continue
                
    except Exception as e:
        print(f"Error in create_google_calendar_event: {e}")
    
async def send_telegram_reminders(ptb_app):
    try:
        async with get_db_connection() as conn:

            today = pendulum.now('Asia/Kolkata').date()
            current_time = pendulum.now('UTC')

            get_all_standard_reminders = """
                                        SELECT u.id as uid, u.telegram_id, u.calendar_enabled, u.telegram_enabled, j.* 
                                        FROM users u JOIN journeys j
                                        ON u.id = j.user_id
                                        WHERE u.telegram_enabled AND (j.release_day_date = $1 OR j.day_before_release_date = $1)
                                        """
            
            standard_reminders = await conn.fetch(get_all_standard_reminders, today)

            for reminder in standard_reminders:
                try:
                    if reminder['release_day_date'] == today and reminder['sent_telegram_reminder_release_day'] is None:
                        await send_message(
                                        ptb_app,
                                        reminder['telegram_id'], 
                                        f"Hii! This is your reminder that tickets for your {reminder['journey_name']} on {reminder['journey_date']} will be released today at 8AM IST"
                                    )
                        await conn.execute(
                                        "UPDATE journeys SET sent_telegram_reminder_release_day = $1 WHERE user_id=$2 AND id=$3", 
                                        current_time, 
                                        reminder['uid'], 
                                        reminder['id']
                                    )
                        
                    if reminder['day_before_release_date'] == today and reminder['sent_telegram_reminder_day_before'] is None:
                        await send_message(
                                        ptb_app,
                                        reminder['telegram_id'], 
                                        f"Hii! This is your reminder that tickets for your {reminder['journey_name']} on {reminder['journey_date']} will be released tomorrow at 8AM IST"
                                    )
                        await conn.execute(
                                        "UPDATE journeys SET sent_telegram_reminder_day_before = $1 WHERE user_id=$2 AND id=$3", 
                                        current_time, 
                                        reminder['uid'], 
                                        reminder['id']
                                    )
                except Exception as e:
                    print(f"Failed to send telegram reminder to user {reminder['uid']}, telegram id {reminder['telegram_id']} for journey {reminder['journey_name']}. Error: {e}")
                    continue
            
            get_all_custom_reminders = """
                                        SELECT u.id as uid, u.telegram_id, j.journey_name, j.journey_date, cr.*
                                        FROM users u
                                        JOIN journeys j ON u.id = j.user_id 
                                        JOIN custom_reminders cr ON j.id = cr.journey_id 
                                        WHERE u.telegram_enabled = TRUE AND u.telegram_id IS NOT NULL
                                        AND cr.sent_telegram_reminder_custom_day IS NULL
                                        AND cr.reminder_date = $1
                                        """
            
            custom_reminders = await conn.fetch(get_all_custom_reminders, today)

            for reminder in custom_reminders:
                try:
                    await send_message(
                                        ptb_app,
                                        reminder['telegram_id'], 
                                        f"Hii! This is your custom reminder for booking train tickets for your {reminder['journey_name']} on {reminder['journey_date']}."
                                    )
                    await conn.execute(
                                    "UPDATE custom_reminders SET sent_telegram_reminder_custom_day = $1 WHERE id=$2", 
                                    current_time, 
                                    reminder['id']
                                )
                except Exception as e:
                    print(f"Failed to send telegram reminder to user {reminder['uid']}, telegram id {reminder['telegram_id']} for journey {reminder['journey_name']}. Error: {e}")
                    continue

    except Exception as e:
        print(f"Error in send_telegram_reminders: {e}")