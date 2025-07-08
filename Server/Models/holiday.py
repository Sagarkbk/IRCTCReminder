from pydantic import BaseModel
from typing import List
from datetime import date

class HolidayBody(BaseModel):
    holiday_name: List[str]
    holiday_date: List[date]
    category: List[str]
    day_before_sent: List[bool]
    release_day_sent: List[bool]

class HolidayResponse(BaseModel):
    holiday_name: str
    holiday_date: date
    category: str
    day_before_sent: bool
    release_day_sent: bool

    class Config:
        from_attributes = True