from fastapi import APIRouter, Response, HTTPException, status
from dotenv import load_dotenv
import os
from Models.auth import GoogleAuth
from Services.authService import userVerification

load_dotenv()
WEB_CLIENT_ID = os.getenv("WEB_CLIENT_ID")

authRouter = APIRouter(prefix="/auth")

@authRouter.post("/google")
async def googleAuth(body: GoogleAuth, response: Response):
    try:
        RECEIVED_CLIENT_ID = body.clientId
        if RECEIVED_CLIENT_ID != WEB_CLIENT_ID:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return "Invalid Client ID"
        data = userVerification(body)
        if data.existingUser and data.user:
            response.status_code = status.HTTP_200_OK
            return data.user
        if data.newUser:
            response.status_code = status.HTTP_200_OK
            return "User created"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)