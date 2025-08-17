from pydantic import BaseModel
from typing import Optional

class UserPreferencesInput(BaseModel):
    calendar_enabled: bool | None = None
    telegram_enabled: bool | None = None