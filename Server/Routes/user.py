from fastapi import APIRouter, Depends, HTTPException, status
from Middlewares.middlewares import authMiddleware
from Services.userService import get_user_by_id, update_user_settings
from fastapi_limiter.depends import RateLimiter

userRouter = APIRouter(prefix="/user")

@userRouter.get("/profile", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=30, seconds=60))])
async def getProfile(user_id: int = Depends(authMiddleware)):
    try:
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@userRouter.put("/preferences", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def updateProfile(body, user_id: int = Depends(authMiddleware)):
    try:
        user = await update_user_settings(user_id, body)
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)