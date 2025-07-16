from fastapi import FastAPI
from dotenv import load_dotenv
from Routes.auth import authRouter
from Routes.user import userRouter
from Routes.journey import journeyRouter
from Routes.integration import integrationRouter
from Routes.telegram import telegramRouter
from Telegram_Bot.bot import bot_initialization
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    ptb_app = bot_initialization()
    await ptb_app.initialize()
    app.state.ptb_app = ptb_app
    print("Bot has been initialized")
    yield
    await app.state.ptb_app.shutdown()
    print("Bot has been shutdown")

app = FastAPI(lifespan=lifespan)

app.include_router(authRouter, prefix="/api")
app.include_router(userRouter, prefix="/api")
app.include_router(journeyRouter, prefix="/api")
app.include_router(integrationRouter, prefix="/api")
app.include_router(telegramRouter, prefix="/api")