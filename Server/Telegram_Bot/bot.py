from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, Application
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from Database.models import Users
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
DATABASE_URl=os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URl)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        return session

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        options = [
            [InlineKeyboardButton("YES", callback_data="enable")],
            [InlineKeyboardButton("NO", callback_data="do_not_enable")],
        ]
        await update.message.reply_text(
            "Do you want to Enable Reminders?",
            reply_markup=InlineKeyboardMarkup(options)
        )
        print("Inside start")
    except Exception as e:
        print(f"Exception in /start: {e}")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        options = [
            [InlineKeyboardButton("YES", callback_data="disable")],
            [InlineKeyboardButton("NO", callback_data="do_not_disable")],
        ]
        await update.message.reply_text(
            "Do you want to Disable Reminders?",
            reply_markup=InlineKeyboardMarkup(options)
        )
        print("Inside stop")
    except Exception as e:
        print(f"Exception in /stop: {e}")

async def commandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        session = await get_db()
        if query:
            await query.answer()
            if query.data in ("enable", "do_not_enable"):
                if query.data == "enable":
                    user = Users(telegram_id=update.effective_user.id)
                    session.add(user)
                    await session.commit()
                    await query.edit_message_text("✅ Reminders are Enabled! Use /stop to disable reminders")
                elif query.data == "do_not_enable":
                    await query.edit_message_text("❌ Reminders are not Enabled! Use /start to enable reminders")
            if query.data in ("disable", "do_not_disable"):
                if query.data == "disable":
                    await query.edit_message_text("✅ Reminders are Disabled! Use /start to enable reminders")
                elif query.data == "do_not_disable":
                    await query.edit_message_text("❌ Reminders are not Disabled! Use /stop to disable reminders")
        print("Inside commandHandler")
    except Exception as e:
        print(f"Exception in /commandHandler: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CallbackQueryHandler(commandHandler))
    app.run_polling(
        poll_interval=2.0, 
        bootstrap_retries=3,)
    print("Inside main")

if __name__=="__main__":
    main()