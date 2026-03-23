from google.oauth2 import id_token
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
import os
from .userService import create_user, get_user_by_google_id, update_user
import jwt
from fastapi import status, HTTPException
import pendulum

WEB_CLIENT_ID = os.getenv("WEB_CLIENT_ID")
WEB_CLIENT_SECRET = os.getenv("WEB_CLIENT_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")

async def userVerification(body, rds=None):
    try:
        flow = Flow.from_client_config(
            client_config={
                "web":{
                    "client_id": WEB_CLIENT_ID,
                    "client_secret": WEB_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["postmessage"],
                }
            },
            scopes=[
                'https://www.googleapis.com/auth/calendar.events',
                'openid',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile'
            ],
            redirect_uri = "postmessage",
        )

        flow.fetch_token(code=body.authCode)
        credentials = flow.credentials
        google_refresh_token = credentials.refresh_token
        
        userInfo = id_token.verify_oauth2_token(credentials.id_token, Request(), WEB_CLIENT_ID, clock_skew_in_seconds=5)

        try:
            existingUser = await get_user_by_google_id(userInfo.get('sub'))
            updatedUser = await update_user(userInfo, existingUser['id'], google_refresh_token, rds)
            jwt_token = createJwtToken(updatedUser)
            return {"existingUser": True, "user": updatedUser, "token": jwt_token}
        except HTTPException as e:
            if e.status_code == 404:
                newUser = await create_user(userInfo, google_refresh_token, rds)
                jwt_token = createJwtToken(newUser)
                return {"existingUser": False, "user": newUser, "token": jwt_token}
            else:
                raise
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
def createJwtToken(user):
    try:
        expires = pendulum.now('UTC').add(days=2)
        jwt_token = jwt.encode(
                            {"user_id": user['id'], "email": user['email'], 
                            "username": user['username'], "exp": expires},
                            JWT_SECRET,
                            algorithm="HS256"
                        )
        return jwt_token
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")