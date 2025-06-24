from fastapi import APIRouter

telegramRouter = APIRouter(prefix="/telegram")

@telegramRouter.get("/")
def telegramHome():
    return "Telegram Views"

@telegramRouter.get("/getTelegramDetails")
def getTelegramDetails(id):
    return f"Telegram Details of user with id={id} : ..."