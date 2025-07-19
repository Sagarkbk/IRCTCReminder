from fastapi import APIRouter, Depends, HTTPException, status
from Middlewares.middlewares import authMiddleware
from Services.integrationService import generateLinkingToken, linkTelegramAccount, validateTokenAndGetUser
from fastapi_limiter.depends import RateLimiter

integrationRouter = APIRouter(prefix="/integration")

@integrationRouter.post("/telegram/generateToken", status_code = status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def generateToken(user_id: int = Depends(authMiddleware)):
    try:
        token = await generateLinkingToken(user_id)
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

@integrationRouter.put("/telegram/linkAccount", status_code = status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def linkAccount(body):
    try:
        if (body.telegram_id is None) or (body.telegram_username is None) or (body.token is None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Telegram ID/Telegram Name/Token are/is missing")
        user = await validateTokenAndGetUser(body.token)
        if user['telegram_id']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your Google and Telegram accounts are already linked.")
        updated_user = await linkTelegramAccount(body, user['id'], body.token)
        return {"user": updated_user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)