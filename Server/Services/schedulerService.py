from fastapi import HTTPException, status, Request
from Telegram_Bot.bot import send_message
from Services.googleCalendarService import create_calendar_event
from Database.connection import get_db_connection
import pendulum
from Models.googleCalendarModel import CalendarEvent

async def create_google_calendar_event():
    try:
        async with get_db_connection() as conn:
            
            get_all_calendar_reminders = """
                                        SELECT u.id as uid, u.google_refresh_token, u.telegram_id, u.calendar_enabled, u.telegram_enabled, j.* 
                                        FROM users u JOIN journeys j
                                        ON u.id = j.user_id
                                        WHERE u.calendar_enabled = TRUE AND (j.reminder_on_release_day = TRUE OR j.reminder_on_day_before = TRUE)
                                        """
            
            calendar_reminders = await conn.fetch(get_all_calendar_reminders)
            
            for reminder in calendar_reminders:
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
                    print(f"Failed while creating calendar event for user {reminder['uid']} for journey {reminder['journey_name']}. Error: {e}")
                    continue
    except Exception as e:
        print(f"Error in create_google_calendar_event: {e}")
    
async def send_telegram_reminders(request: Request):
    try:
        async with get_db_connection() as conn:

            today = pendulum.now('UTC').date()

            get_all_telegram_reminders = """"
                                        SELECT u.id as uid, u.google_refresh_token, u.telegram_id, u.calendar_enabled, u.telegram_enabled, j.* 
                                        FROM users u JOIN journeys j
                                        ON u.id = j.user_id
                                        WHERE u.telegram_enabled AND (j.release_day_date = $1 OR j.day_before_release_date = $1)
                                        """
            
            telegram_reminders = await conn.fetch(get_all_telegram_reminders, today)

            for reminder in telegram_reminders:
                try:
                    if reminder['release_day_date'] == today and not reminder['sent_telegram_reminder_release_day']:
                        await send_message(
                                        request.app.state.ptb_app, 
                                        reminder['telegram_id'], 
                                        f"Hii! This is your reminder that tickets for your {reminder['journey_name']} on {reminder['journey_date']} will be released today at 8AM IST"
                                    )
                        await conn.execute(
                                        "UPDATE journeys SET sent_telegram_reminder_release_day = TRUE WHERE user_id=$1 AND id=$2", 
                                        reminder['uid'], 
                                        reminder['id']
                                    )
                        
                    if reminder['day_before_release_date'] == today and not reminder['sent_telegram_reminder_day_before']:
                        await send_message(
                                        request.app.state.ptb_app, 
                                        reminder['telegram_id'], 
                                        f"Hii! This is your reminder that tickets for your {reminder['journey_name']} on {reminder['journey_date']} will be released tomorrow at 8AM IST"
                                    )
                        await conn.execute(
                                        "UPDATE journeys SET sent_telegram_reminder_day_before = TRUE WHERE user_id=$1 AND id=$2", 
                                        reminder['uid'], 
                                        reminder['id']
                                    )
                except Exception as e:
                    print(f"Failed to send telegram reminder to user {reminder['uid']}, telegram id {reminder['telegram_id']} for journey {reminder['journey_name'
                    ]}. Error: {e}")
                    continue
    except Exception as e:
        print(f"Error in send_telegram_reminders: {e}")