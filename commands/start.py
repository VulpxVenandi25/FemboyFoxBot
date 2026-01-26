from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Saluda al usuario"""
    await update.message.reply_text("¡Hola! Usa /novels para ver el catálogo disponible.") # type: ignore