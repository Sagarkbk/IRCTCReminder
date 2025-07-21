from fastapi import APIRouter, Response, HTTPException, status, Depends
import os
from Services.authService import userVerification
from fastapi_limiter.depends import RateLimiter
from Services.redisService import get_redis
from redis.asyncio import Redis
from Models.authModel import GoogleAuth

WEB_CLIENT_ID = os.getenv("WEB_CLIENT_ID")

authRouter = APIRouter(prefix="/auth")

@authRouter.post("/google", status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def googleAuth(body: GoogleAuth, response: Response, rds: Redis = Depends(get_redis)):
    try:
        RECEIVED_CLIENT_ID = body.clientId

        if RECEIVED_CLIENT_ID != WEB_CLIENT_ID:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Client ID")
        
        result = await userVerification(body, rds)

        if result['existingUser']:
            response.status_code = status.HTTP_200_OK
        
        return {"data" : {"user": result['user'], "token": result['token']}}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")