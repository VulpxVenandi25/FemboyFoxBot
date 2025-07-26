from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from dotenv import load_dotenv
import os

load_dotenv()
api_token = os.environ.get("API_TOKEN")

async def say_hellow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola putos!!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


application = ApplicationBuilder().token(api_token).build()

application.add_handler(CommandHandler("start", say_hellow))
application.add_handler(CommandHandler("echo", echo))

application.run_polling(allowed_updates=Update.ALL_TYPES)