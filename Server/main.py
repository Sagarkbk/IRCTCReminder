from fastapi import FastAPI
from dotenv import load_dotenv
from Routes.auth import authRouter
from Routes.user import userRouter
from Routes.journey import journeyRouter
from Routes.integration import integrationRouter
from Routes.telegram import telegramRouter
from Routes.health import healthRouter
from Telegram_Bot.bot import bot_initialization
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Services.schedulerService import create_google_calendar_event, send_telegram_reminders
from fastapi.middleware.cors import CORSMiddleware
from telegram import Update
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_pool = redis.ConnectionPool.from_url("redis://localhost:6379", max_connections=20, encoding="utf8", decode_responses=True)
    redis_connection = redis.Redis(connection_pool=redis_pool)

    await FastAPILimiter.init(redis_connection)
    app.state.redis_client = redis_connection
    print("FastAPILimiter has been initialized")

    ptb_app = bot_initialization()
    await ptb_app.initialize()

    ptb_app.bot_data['rds'] = redis_connection

    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    if WEBHOOK_URL:
        full_webhook_url = f"{WEBHOOK_URL}/api/telegram/webhook"
        await ptb_app.bot.set_webhook(
            url=full_webhook_url,
            allowed_updates=Update.ALL_TYPES
        )
        print(f"Telegram webhook set to: {full_webhook_url}")
    else:
        print("WARNING: WEBHOOK_URL environment variable not set. Bot will not receive updates.")

    app.state.ptb_app = ptb_app
    print("Bot has been initialized")

    scheduler = AsyncIOScheduler(timezone='Asia/Kolkata')
    scheduler.add_job(send_telegram_reminders, 'cron', hour='6,7,8', minute='0', args=[ptb_app])
    scheduler.add_job(create_google_calendar_event, 'cron', hour='*', minute='0')

    scheduler.start()
    print("Scheduler has started")

    yield

    scheduler.shutdown()
    print("Scheduler has shutdown")

    await FastAPILimiter.close()
    print("FastAPILimiter has been closed")

    await redis_pool.disconnect()
    print("Redis pool disconnected")

    await app.state.ptb_app.shutdown()
    print("Bot has been shutdown")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authRouter, prefix="/api")
app.include_router(userRouter, prefix="/api")
app.include_router(journeyRouter, prefix="/api")
app.include_router(integrationRouter, prefix="/api")
app.include_router(telegramRouter, prefix="/api")
app.include_router(healthRouter, prefix="/api")