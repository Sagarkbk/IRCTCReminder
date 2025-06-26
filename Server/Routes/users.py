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

@usersRouter.get("/getUser/{google_id}")
async def getUser(google_id: str):
    try:
        await db.connect()
        get_user_query = """
                SELECT * FROM users WHERE google_id = $1
                """
        existingUser = await db.fetchone(get_user_query, google_id)
        if not existingUser:
            return "User does not exist"
        return {"User Details" : existingUser}
    except Exception as e:
        print(f"Exception when hitting /getUser: {e}")
        raise

@usersRouter.get("/getAllUsers")
async def getAllUsers():
    try:
        await db.connect()
        get_user_query = """
                SELECT * FROM users
                """
        users = await db.fetchall(get_user_query)
        if not users:
            return "No users as of now"
        return {"Users" : users}
    except Exception as e:
        print(f"Exception when hitting /getAllUsers: {e}")
        raise

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