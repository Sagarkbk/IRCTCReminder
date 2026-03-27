from fastapi import APIRouter, Depends, HTTPException, status
from Middlewares.middlewares import authMiddleware
from Services.integrationService import generateLinkingToken, linkTelegramAccount, validateTokenAndGetUser
from fastapi_limiter.depends import RateLimiter
from Services.redisService import get_redis
from redis.asyncio import Redis

integrationRouter = APIRouter(prefix="/integration")

@integrationRouter.post("/telegram/generateToken", status_code = status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def generateToken(user_id: int = Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        print("Reached /telegram/generateToken")
        token = await generateLinkingToken(user_id, rds)
        return {"data": token}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# @integrationRouter.put("/telegram/linkAccount", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=20, seconds=60))])
# async def linkAccount(body: TelegramLinkInput, rds: Redis = Depends(get_redis)):
#     try:
#         print("Reached /telegram/linkAccount")
#         user = await validateTokenAndGetUser(body.token, rds)
#         print(f"Received user: {user}")
#         if user.get('telegram_id') and user.get('telegram_enabled'):
#             print("Inside if block")
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your Google and Telegram accounts are already linked.")
#         print("Before calling linkTelegramAccount")
#         updated_user = await linkTelegramAccount(user['id'], body.telegram_id, body.telegram_username, body.token, rds)
#         print("After calling linkTelegramAccount")
#         return {"data": updated_user}
#     except HTTPException:
#         raise
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")