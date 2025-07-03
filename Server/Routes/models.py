from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    google_id: str;
    email: str;
    username: str;
    reminder_days: Optional[int] = 1;
    calendar_enabled: Optional[bool] = False;

class LinkAccounts(BaseModel):
    token: str;
    telegram_id: int;
    telegram_username: str;

class Holidays(BaseModel):
    user_id: int;
    holiday_name: list[str];
    holiday_date: list[datetime];
    category: list[str];
    day_before_sent: list[Optional[bool]] = False;
    release_day_sent: list[Optional[bool]] = True;