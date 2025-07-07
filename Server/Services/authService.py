from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
import os
from .userService import create_user, get_user

load_dotenv
WEB_CLIENT_ID = os.getenv("WEB_CLIENT_ID")

async def userVerification(body):
    try:
        userInfo = id_token.verify_oauth2_token(body.idToken, requests.Request, WEB_CLIENT_ID)
        existingUser = await get_user(userInfo)
        if existingUser:
            return {"existingUser": True, "newUser": False, "user": existingUser}
        data = await create_user(userInfo)
        return data
    except Exception as e:
        raise e