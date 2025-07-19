from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, Application
import os

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
    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again later.")

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
    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again later.")

async def commandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        if query:
            await query.answer()
            if query.data in ("enable", "do_not_enable"):
                if query.data == "enable":
                    await query.edit_message_text("✅ Reminders are Enabled! Use /stop to disable reminders")
                elif query.data == "do_not_enable":
                    await query.edit_message_text("❌ Reminders are not Enabled! Use /start to enable reminders")
            if query.data in ("disable", "do_not_disable"):
                if query.data == "disable":
                    await query.edit_message_text("✅ Reminders are Disabled! Use /start to enable reminders")
                elif query.data == "do_not_disable":
                    await query.edit_message_text("❌ Reminders are not Disabled! Use /stop to disable reminders")
    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again later.")

def bot_initialization():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise ValueError("Telegram bot token not found in environment variables.")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CallbackQueryHandler(commandHandler))
    return app