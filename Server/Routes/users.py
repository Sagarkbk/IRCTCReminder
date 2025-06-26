from fastapi import APIRouter, Body
from pydantic import BaseModel
from Database.connection import db

class User(BaseModel):
    google_id: str;
    email: str;
    username: str;
    reminder_days: int;
    calendar_enabled: bool;
    telegram_enabled: bool;

usersRouter = APIRouter(prefix="/users")

@usersRouter.post("/addUser")
async def addUser(body: User):
    try:
        await db.connect()
        insert_user_query = """
                INSERT INTO users (google_id, email, username, reminder_days, calendar_enabled, telegram_enabled) VALUES ($1, $2, $3, $4, $5, $6)
                """
        await db.execute(insert_user_query, body.google_id, body.email, body.username, body.reminder_days, body.calendar_enabled, body.telegram_enabled)
        get_user_query = """
                SELECT * FROM users WHERE google_id = $1
                """
        newUser = await db.fetchone(get_user_query, body.google_id)
        return {"newUser" : newUser}
    except Exception as e:
        return f"Exception: {e}"