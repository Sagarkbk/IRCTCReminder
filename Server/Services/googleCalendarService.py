import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from fastapi import status, HTTPException
from Models.googleCalendarModel import CalendarEvent

WEB_CLIENT_ID = os.getenv("WEB_CLIENT_ID")
WEB_CLIENT_SECRET = os.getenv("WEB_CLIENT_SECRET")

async def get_calendar_service(refresh_token: str):
    try:
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        creds = Credentials.from_authorized_user_info(
            info={
                "refresh_token": refresh_token,
                "client_id": WEB_CLIENT_ID,
                "client_secret": WEB_CLIENT_SECRET
            },
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )

        service = build('calendar', 'v3', credentials=creds, static_discovery=False)
        return service
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def create_calendar_event(details: CalendarEvent):
    try:
        event = {
            "summary": details.summary,
            "description": details.desc,
            "start":{
                "dateTime": details.start_time,
                "timeZone": "Asia/Kolkata",
            },
            "end":{
                "dateTime": details.end_time,
                "timeZone": "Asia/Kolkata",
            }
        }
        calendar_service = get_calendar_service()
        event = calendar_service.events().insert(calenderId='primary', body=event).execute()
        return event['id']
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
async def update_calendar_event(eventId: str, details: CalendarEvent):
    try:
        event = {
            "summary": details.summary,
            "description": details.desc,
            "start":{
                "dateTime": details.start_time,
                "timeZone": "Asia/Kolkata",
            },
            "end":{
                "dateTime": details.end_time,
                "timeZone": "Asia/Kolkata",
            }
        }
        calendar_service = get_calendar_service()
        event = calendar_service.events().update(calenderId='primary', eventId=eventId, body=event).execute()
        return True
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def deletee_calendar_event(eventId: str):
    try:
        calendar_service = get_calendar_service()
        event = calendar_service.events().delete(calenderId='primary', eventId=eventId).execute()
        return True
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")