from fastapi import APIRouter, HTTPException, status, Request
from telegram import Update

telegramRouter = APIRouter(prefix="/telegram")

@telegramRouter.post("/webhook", status_code=status.HTTP_200_OK)
async def telegram_webhook(request: Request):
    try:
        ptb_app = request.app.state.ptb_app
        data = await request.json()
        update = Update.de_json(data=data, bot=ptb_app.bot)
        await ptb_app.process_update(update)
        return
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)