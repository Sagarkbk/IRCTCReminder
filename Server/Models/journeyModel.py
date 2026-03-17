from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class JourneyInput(BaseModel):
    journey_name         : str
    journey_date         : date
    reminder_on_release_day: bool
    reminder_on_day_before : bool
    custom_dates         : List[date] = Field(default_factory=list)