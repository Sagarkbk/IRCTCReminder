from pydantic import BaseModel

class TelegramLinkInput(BaseModel):
    telegram_id      : int
    telegram_username: str
    token            : str