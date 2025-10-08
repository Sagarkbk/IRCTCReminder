from fastapi import APIRouter, HTTPException, status, Request, Depends
from telegram import Update
from fastapi_limiter.depends import RateLimiter

telegramRouter = APIRouter(prefix="/telegram")

@telegramRouter.post("/webhook", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=1000, seconds=60))])
async def telegram_webhook(request: Request):
    try:
        print("Reached /webhook")
        ptb_app = request.app.state.ptb_app
        data = await request.json()
        update = Update.de_json(data=data, bot=ptb_app.bot)
        await ptb_app.process_update(update)
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)