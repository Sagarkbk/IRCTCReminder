from pydantic import BaseModel
from typing import Optional

class UserPreferencesInput(BaseModel):
    calendar_enabled: Optional[bool]
    telegram_enabled: Optional[bool]