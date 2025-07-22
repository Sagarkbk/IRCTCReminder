from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, Application
import os
from Services.userService import update_user_settings, get_user_by_telegram_id
from Services.integrationService import validateTokenAndGetUser, linkTelegramAccount
from Models.userModel import UserPreferencesInput
from fastapi import HTTPException, Depends
from Services.redisService import get_redis
from redis.asyncio import Redis
import httpx

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

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE, rds: Redis = Depends(get_redis)):
    try:
        if not context.args:
            await update.message.reply_text("To link your account, please use the link provided on our website.")
        
        token = context.args[0]

        try:
            telegram_id = await update.message.from_user.id
            telegram_username = await update.message.from_user.username
            API_URL = os.getenv("API_URL")
            payload = {
                "token": token,
                "telegram_id": telegram_id,
                "telegram_username": telegram_username
            }

            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{API_URL}/api/integration/telegram/linkAccount", 
                    json=payload
                    )
                response.raise_for_status()
                await update.message.reply_text("Success! Your telegram account is now linked.")
        except httpx.HTTPStatusError as e:
            await update.message.reply_text(e.response.json().get("detail"))
        except httpx.RequestError:
            await update.message.reply_text("An error occurred. Please try again later.")
    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again later.")

async def commandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE, rds: Redis = Depends(get_redis)):
    try:
        query = update.callback_query
        if query:
            await query.answer()
            telegram_id = update.callback_query.from_user.id
            user = await get_user_by_telegram_id(telegram_id)
            if query.data in ("enable", "do_not_enable"):
                if query.data == "enable":
                    user_prefs = UserPreferencesInput(telegram_enabled=True)
                    await update_user_settings(user['id'], user_prefs, rds)
                    await query.edit_message_text("✅ Reminders are Enabled! Use /stop to disable reminders")
                elif query.data == "do_not_enable":
                    await query.edit_message_text("❌ Reminders are not Enabled! Use /start to enable reminders")
            if query.data in ("disable", "do_not_disable"):
                if query.data == "disable":
                    user_prefs = UserPreferencesInput(telegram_enabled=False)
                    await update_user_settings(user['id'], user_prefs, rds)
                    await query.edit_message_text("✅ Reminders are Disabled! Use /start to enable reminders")
                elif query.data == "do_not_disable":
                    await query.edit_message_text("❌ Reminders are not Disabled! Use /stop to disable reminders")
    except HTTPException as e:
        if e.status_code == 404:
            await update.callback_query.edit_message_text("Your telegram account is not associated with any of our website account. Please create an account on our website and try again")
        else:
            await update.callback_query.edit_message_text(f"An unexpected error occurred: {e.detail}. Please try again later.")
    except Exception as e:
        await update.callback_query.edit_message_text("An unexpected error occurred. Please try again later.")

def bot_initialization():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise ValueError("Telegram bot token not found in environment variables.")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("link", link))
    app.add_handler(CallbackQueryHandler(commandHandler))
    return app