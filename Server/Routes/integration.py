from fastapi import APIRouter, Depends, HTTPException, status
from Middlewares.middlewares import authMiddleware
from Services.integrationService import generateLinkingToken, linkTelegramAccount, validateTokenAndGetUser

integrationRouter = APIRouter(prefix="/user")

@integrationRouter.post("/telegram/generateToken")
async def generateToken(user_id: int = Depends(authMiddleware)):
    try:
        token = await generateLinkingToken(user_id)
        return token
    except Exception as e:
        raise

@integrationRouter.put("/telegram/linkAccount")
async def linkAccount(body):
    try:
        user = await validateTokenAndGetUser(body.token)
        if user['telegram_id']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your Google and Telegram accounts are already linked.")
        updated_user = await linkTelegramAccount(body, user['id'], body.token)
        return updated_user
    except Exception as e:
        raise