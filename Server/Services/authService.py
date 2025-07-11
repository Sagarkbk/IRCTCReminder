from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
import os
from .userService import create_user, get_user_by_google_id, update_user
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import status, HTTPException

load_dotenv
WEB_CLIENT_ID = os.getenv("WEB_CLIENT_ID")
JWT_SECRET = os.getenv("JWT_SECRET")

async def userVerification(body):
    try:
        userInfo = id_token.verify_oauth2_token(body.idToken, requests.Request, WEB_CLIENT_ID)

        existingUser = await get_user_by_google_id(userInfo.get('sub'))

        if existingUser:
            updatedUser = await update_user(userInfo, existingUser['id'])
            jwt_token = createJwtToken(updatedUser)
            return {"existingUser": True, "user": updatedUser, "token": jwt_token}
        
        newUser = await create_user(userInfo)
        jwt_token = createJwtToken(newUser)
        return {"existingUser": False, "user": newUser, "token": jwt_token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    
def createJwtToken(user):
    try:
        expires = datetime.now(timezone.utc) + timedelta(days=2)
        jwt_token = jwt.encode(
                            {"user_id": user.id, "email": user.email, 
                            "username": user.username, "exp": expires},
                            JWT_SECRET,
                            algorithm="HS256"
                        )
        return jwt_token
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)