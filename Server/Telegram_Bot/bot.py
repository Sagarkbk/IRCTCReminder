from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, Application
import os
from Services.userService import update_user_settings, get_user_by_telegram_id
from Services.journeyService import get_existing_journeys
from Models.userModel import UserPreferencesInput
from fastapi import HTTPException
import pendulum
from Services.integrationService import validateTokenAndGetUser, linkTelegramAccount

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Reached help")
        message = """*Welcome! Here are the available commands:*

`/start   ` - Enable reminders.
`/stop    ` - Disable reminders.
`/journeys` - Lists all of your journeys.
`/help    ` - Shows this help message.

To link your account, please click the "Link Telegram" button on our website. This will bring you here and automatically link your account."""

        await update.message.reply_text(message, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again later.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Reached start")
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
        print("Reached stop")
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

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Reached link")
        if not context.args:
            await update.message.reply_text("To link your account, please use the link provided on our website.")
            return
        
        token = context.args[0]
        
        telegram_id = update.message.from_user.id
        telegram_username = update.message.from_user.username

        rds = context.bot_data.get('rds')

        try:
            user = await validateTokenAndGetUser(token, rds=rds)

            if user.get('telegram_id') and user.get('telegram_enabled'):
                await update.message.reply_text("Your Google and Telegram accounts are already linked.")
                return

            await linkTelegramAccount(user['id'], telegram_id, telegram_username, token, rds=rds)
            await update.message.reply_text("Success! Your telegram account is now linked.")

            welcome_message = """*Welcome! Here are the available commands:*

`/start   ` - Enable reminders.
`/stop    ` - Disable reminders.
`/journeys` - Lists all of your journeys.
`/help    ` - Shows this help message."""

            await update.message.reply_text(welcome_message, parse_mode='Markdown')
        
        except HTTPException as e:
            await update.message.reply_text(f"{e.detail}")
        
        except Exception as e:
            await update.message.reply_text("An error occurred during linking. Please try again later.")

    except Exception as e:
        await update.message.reply_text("An error occurred. Please try again later.")

async def journeys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("Reached journeys")
        telegram_id = update.message.from_user.id
        rds = context.bot_data.get('rds')
        user = await get_user_by_telegram_id(telegram_id, rds)
        journeys = await get_existing_journeys(user['id'], rds)
        if len(journeys) == 0:
            await update.message.reply_text("You don't have any journeys to be reminded")
            return
        
        message = "Here are your upcoming journeys:\n\n"
        
        for journey in journeys:
            j_date = pendulum.parse(str(journey['journey_date'])).format('DD MMM YYYY')
            message += f"*{journey['journey_name']}* ({j_date})\n"
            reminders = []
            if journey['reminder_on_release_day']:
                reminders.append(pendulum.parse(str(journey['release_day_date'])))
            if journey['reminder_on_day_before']:
                reminders.append(pendulum.parse(str(journey['day_before_release_date'])))
            if journey['custom_reminders']:
                for reminder in journey['custom_reminders']:
                    reminders.append(pendulum.parse(str(reminder['reminder_date'])))
            if reminders:
                unique_reminders = sorted(list(set(reminders)))
                rem_dates = [r.format('DD MMM YYYY') for r in unique_reminders]
                message += f"Reminders: {', '.join(rem_dates)}\n\n"
            else:
                message += "No reminders set for this journey\n\n"

        await update.message.reply_text(message, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("An unexpected error occurred. Please try again later.")

async def send_message(bot_app: Application, telegram_id: int, message: str):
    try:
        await bot_app.bot.send_message(chat_id=telegram_id, text=message)
        return True
    except Exception as e:
        return False

async def commandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        rds = context.bot_data.get('rds')
        if query:
            await query.answer()
            telegram_id = update.callback_query.from_user.id
            user = await get_user_by_telegram_id(telegram_id, rds)
            if query.data in ("enable", "do_not_enable"):
                if query.data == "enable":
                    if user.get('telegram_enabled'):
                        await query.edit_message_text("✅ Reminders are already enabled!")
                    else:
                        user_prefs = UserPreferencesInput(telegram_enabled=True)
                        await update_user_settings(user['id'], user_prefs, rds)
                        await query.edit_message_text("✅ Reminders are now Enabled! Use /stop to disable reminders")
                elif query.data == "do_not_enable":
                    await query.edit_message_text("No changes made.")
            elif query.data in ("disable", "do_not_disable"):
                if query.data == "disable":
                    user_prefs = UserPreferencesInput(telegram_enabled=False)
                    await update_user_settings(user['id'], user_prefs, rds)
                    await query.edit_message_text("❌ Reminders are disabled and your account has been unlinked. Visit the website to reconnect!")
                elif query.data == "do_not_disable":
                    await query.edit_message_text("No changes made. Your reminders are still active! ✅")
            else:
                await query.edit_message_text("❌ Not a valid button.")
    except HTTPException as e:
        if e.status_code == 404:
            await update.callback_query.edit_message_text("❌ Account not found. It may have been unlinked. Please reconnect from our website!")
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
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("journeys", journeys))
    app.add_handler(CallbackQueryHandler(commandHandler))
    return app