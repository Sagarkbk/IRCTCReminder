from fastapi import APIRouter, Body
from pydantic import BaseModel
from Database.connection import Database

class User(BaseModel):
    google_id: str;
    email: str;
    username: str;
    reminder_days: int;
    calendar_enabled: bool;
    telegram_enabled: bool;

usersRouter = APIRouter(prefix="/users")

@usersRouter.get("/")
def usersHome():
    return "Users Views"

@usersRouter.get("/getUserDetails")
async def getUserDetails(body: User):
    return body