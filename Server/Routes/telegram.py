from fastapi import APIRouter, HTTPException, status, Request, Depends
from telegram import Update
from fastapi_limiter.depends import RateLimiter
import os
from dotenv import load_dotenv

load_dotenv()

telegramRouter = APIRouter(prefix="/telegram")

@telegramRouter.post("/webhook", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=1000, seconds=60))])
async def telegram_webhook(request: Request):
    header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    expected_token = os.getenv("TELEGRAM_SECRET_TOKEN")

    if header_token != expected_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized request")

    try:
        ptb_app = request.app.state.ptb_app
        data = await request.json()
        update = Update.de_json(data=data, bot=ptb_app.bot)
        await ptb_app.process_update(update)
        return
    except Exception as e:
        print(f"Error in telegram_webhook: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")