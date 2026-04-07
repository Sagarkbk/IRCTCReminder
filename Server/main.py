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
from telegram.error import RetryAfter
from Database.connection import init_pool, close_pool
from Database.migrations_runner import Migrations
import os
import asyncio

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()

    REDIS_URL = os.getenv("REDIS_URL")
    if not REDIS_URL:
        REDIS_URL = "redis://localhost:6379"
    redis_pool = redis.ConnectionPool.from_url(REDIS_URL, max_connections=20, encoding="utf8", decode_responses=True)
    redis_connection = redis.Redis(connection_pool=redis_pool)

    await FastAPILimiter.init(redis_connection)
    app.state.redis_client = redis_connection
    print("FastAPILimiter has been initialized")

    ptb_app = bot_initialization()
    await ptb_app.initialize()

    ptb_app.bot_data['rds'] = redis_connection

    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    TELEGRAM_SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")

    if not TELEGRAM_SECRET_TOKEN:
        raise ValueError("TELEGRAM_SECRET_TOKEN is missing! Bot cannot start securely.")

    if WEBHOOK_URL:
        full_webhook_url = f"{WEBHOOK_URL}/api/telegram/webhook"
        try:
            await ptb_app.bot.set_webhook(
            url=full_webhook_url,
            allowed_updates=Update.ALL_TYPES,
            secret_token=TELEGRAM_SECRET_TOKEN
            )
            print(f"Telegram webhook set to: {full_webhook_url}")
        except RetryAfter as e:
            print(f"Flood control: Webhook setup already handled by another worker. Sleeping {e.retry_after}s...")
            await asyncio.sleep(e.retry_after)
        except Exception as e:
            print(f"Unexpected error setting webhook: {e}")
    else:
        print("WARNING: WEBHOOK_URL environment variable not set. Bot will not receive updates.")

    app.state.ptb_app = ptb_app
    print("Bot has been initialized")

    is_master = await redis_connection.set("irctc:scheduler_lock", "active", nx=True, ex=600)

    if is_master:
        migration_runner = Migrations()
        await migration_runner.run_pending_migrations()
        print(f"PRIMARY WORKER: Database migrations checked/applied by worker {os.getpid()}")

        scheduler = AsyncIOScheduler(timezone='Asia/Kolkata')
        scheduler.add_job(send_telegram_reminders, 'cron', hour='6,7,8', minute='0', args=[ptb_app])
        scheduler.add_job(create_google_calendar_event, 'cron', hour='*', minute='0')
        scheduler.start()
        app.state.scheduler = scheduler
        print(f"PRIMARY WORKER: Scheduler started on worker {os.getpid()}")
    else:
        app.state.scheduler = None
        print("Scheduler already started by another worker. Skipping...")

    yield

    await close_pool()

    if app.state.scheduler:
        app.state.scheduler.shutdown()
        await redis_connection.delete("irctc:scheduler_lock")
        print("Scheduler has shutdown and lock cleared")
    else:
        print("Worker shutdown complete")

    await FastAPILimiter.close()
    print("FastAPILimiter has been closed")

    await redis_pool.disconnect()
    print("Redis pool disconnected")

    await app.state.ptb_app.shutdown()
    print("Bot has been shutdown")

app = FastAPI(lifespan=lifespan)

frontend_urls_str = os.getenv("FRONTEND_URLS", "")
origins = [url.strip() for url in frontend_urls_str.split(",") if url.strip()]

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