from pydantic import BaseModel

class TelegramLinkInput(BaseModel):
    telegram_id      : int
    telegram_username: str | None = None
    token            : str