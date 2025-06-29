from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from Database.connection import db
import pytz

class User(BaseModel):
    google_id: str;
    email: str;
    username: str;
    reminder_days: Optional[int] = 1;
    calendar_enabled: Optional[bool] = False;

class Telegram(BaseModel):
    telegram_id: int;
    telegram_username: str;
    telegram_linked_at: str;
    telegram_enabled: Optional[bool] = False;
    preferences_updated_at: datetime

class LinkAccounts(BaseModel):
    token: str;
    telegram_id: int;
    telegram_username: str;

usersRouter = APIRouter(prefix="/users")

@usersRouter.get("/getUser/{google_id}")
async def getUser(google_id: str, response: Response):
    try:
        await db.connect()
        get_user_query = """
                SELECT * FROM users WHERE google_id = $1
                """
        existingUser = await db.fetchone(get_user_query, google_id)
        if not existingUser:
            response.status_code = status.HTTP_404_NOT_FOUND
            return "User does not exist"
        response.status_code = status.HTTP_200_OK
        return {"User Details" : existingUser}
    except Exception as e:
        print(f"Exception when hitting /getUser: {e}")
        raise

@usersRouter.get("/getAllUsers")
async def getAllUsers(response: Response):
    try:
        await db.connect()
        get_users_query = """
                SELECT * FROM users
                """
        response.status_code = status.HTTP_200_OK
        users = await db.fetchall(get_users_query)
        if not users:
            return "No users as of now"
        return {"Users" : users}
    except Exception as e:
        print(f"Exception when hitting /getAllUsers: {e}")
        raise

@usersRouter.post("/addUser")
async def addUser(body: User, response: Response):
    try:
        await db.connect()
        get_user_with_googleid_query = """
                SELECT * FROM users WHERE google_id = $1
                """
        existingUserWithId = await db.fetchone(get_user_with_googleid_query, body.google_id)
        if existingUserWithId:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return "User already exists with provided Google ID"
        get_user_with_email_query = """
                SELECT * FROM users WHERE email = $1
                """
        existingUserWithEmail = await db.fetchone(get_user_with_email_query, body.email)
        if existingUserWithEmail:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return "User already exists with provided Email"
        insert_user_query = """
                INSERT INTO users (google_id, email, username, reminder_days, calendar_enabled) VALUES ($1, $2, $3, $4, $5)
                """
        await db.execute(insert_user_query, body.google_id, body.email, body.username, body.reminder_days, body.calendar_enabled)
        get_user_query = """
                SELECT * FROM users WHERE google_id = $1
                """
        newUser = await db.fetchone(get_user_query, body.google_id)
        response.status_code = status.HTTP_201_CREATED
        return {"newUser" : newUser}
    except Exception as e:
        print(f"Exception when hitting /addUser: {e}")
        raise

@usersRouter.post("/generateToken/{google_id}")
async def generateToken(google_id, response: Response):
    try:
        await db.connect()
        get_user_with_googleid_query = """
                SELECT * FROM users WHERE google_id = $1
                """
        existingUserWithId = await db.fetchone(get_user_with_googleid_query, google_id)
        if not existingUserWithId:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return "There is no user with provided Google ID"
        check_if_token_exists_query = """
                SELECT * FROM google_telegram_link WHERE user_id = $1
                """
        unusedToken = await db.fetchone(check_if_token_exists_query, existingUserWithId['id'])
        current_time = datetime.now(pytz.UTC)
        expires_at = current_time + timedelta(minutes=30)
        if unusedToken and (not unusedToken['is_used']) and (unusedToken['expires_at'] > current_time):
            response.status_code = status.HTTP_200_OK
            return {"Unused/Non-Expired Token" : unusedToken['token']}
        if unusedToken and (unusedToken['is_used'] or (unusedToken['expires_at'] < current_time)):
            delete_expired_or_used_token_query = """
                DELETE FROM google_telegram_link WHERE user_id = $1
                """
            await db.execute(delete_expired_or_used_token_query, existingUserWithId['id'])
        # For now creating token by combining gid and user id
        token = f"{google_id}#{existingUserWithId['id']}"
        insert_token_query = """
                INSERT INTO google_telegram_link (user_id, token, expires_at) VALUES ($1, $2, $3)
                """
        await db.execute(insert_token_query, existingUserWithId['id'], token, expires_at)
        response.status_code = status.HTTP_201_CREATED
        return {"Token" : token}

    except Exception as e:
        print(f"Exception when hitting /generateToken: {e}")
        raise

@usersRouter.post("/linkAccounts")
async def linkAccounts(body: LinkAccounts, response: Response):
    try:
        if not body.token:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return "Please come to telegram through the link from website so that we can link your google and telegram accounts"
        await db.connect()
        get_token_details_query = """
                SELECT * from google_telegram_link WHERE
                token = $1
                """
        token_details = await db.fetchone(get_token_details_query, body.token)
        if token_details['is_used']:
            return "Your google and telegram accounts have already been linked. Linking is no longer required"
        current_time = datetime.now(pytz.UTC)
        if token_details['expires_at'] > current_time:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return "Your session token has expired. Please come to telegram through the link from website so that we can link your google and telegram accounts"
        link_accounts_query = """
                UPDATE TABLE users SET telegram_id = $1 AND telegram_username = $2 AND
                telegram_linked_at = $3 AND preferences_updated_at = $4 WHERE id = $5
                """
        await db.execute(link_accounts_query, body.telegram_id, body.telegram_username, current_time, current_time, token_details['user_id'])
        response.status_code = status.HTTP_201_CREATED
        return "Added telegram details"
    except Exception as e:
        print(f"Exception when hitting /linkAccounts: {e}")
        raise