from pydantic import BaseModel
from datetime import datetime

class CalendarEvent(BaseModel):
    summary: str
    desc: str
    start_time: datetime
    end_time: datetime
    reminders: dict