from fastapi import APIRouter, Depends, HTTPException, status
from Middlewares.middlewares import authMiddleware
from Services.userService import get_user_by_id, update_user_settings
from fastapi_limiter.depends import RateLimiter
from Services.redisService import get_redis
from redis.asyncio import Redis
from Models.userModel import UserPreferencesInput

userRouter = APIRouter(prefix="/user")

@userRouter.get("/profile", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=30, seconds=60))])
async def getProfile(user_id: int = Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        user = await get_user_by_id(user_id, rds)
        return {"data" : user}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in getProfile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@userRouter.put("/preferences", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def updateProfile(body: UserPreferencesInput, user_id: int = Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        user = await update_user_settings(user_id, body, rds)
        return {"data" : user}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in updateProfile: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")