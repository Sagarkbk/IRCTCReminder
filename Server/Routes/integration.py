from fastapi import APIRouter, Depends, HTTPException, status
from Middlewares.middlewares import authMiddleware
from Services.integrationService import generateLinkingToken, linkTelegramAccount, validateTokenAndGetUser
from fastapi_limiter.depends import RateLimiter
from Services.redisService import get_redis
from redis.asyncio import Redis
from Models.telegramModel import TelegramLinkInput

integrationRouter = APIRouter(prefix="/integration")

@integrationRouter.post("/telegram/generateToken", status_code = status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def generateToken(user_id: int = Depends(authMiddleware), rds: Redis = Depends(get_redis)):
    try:
        token = await generateLinkingToken(user_id, rds)
        return {"data": token}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@integrationRouter.put("/telegram/linkAccount", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def linkAccount(body: TelegramLinkInput, rds: Redis = Depends(get_redis)):
    try:
        user = await validateTokenAndGetUser(body.token, rds)
        if user['telegram_id']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your Google and Telegram accounts are already linked.")
        updated_user = await linkTelegramAccount(body, user['id'], body.token, rds)
        return {"data": updated_user}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")