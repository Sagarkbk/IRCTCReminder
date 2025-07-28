from pydantic import BaseModel
from datetime import date

class CalendarEvent(BaseModel):
    summary: str
    desc: str
    start_time: date
    end_time: date
    reminders: dict