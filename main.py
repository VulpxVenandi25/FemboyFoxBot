from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from commands.start import start
from commands.get_novels import get_novels
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración de credenciales
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # type: ignore
SUPABASE_URL = os.environ.get("SUPABASE_URL")  # type: ignore
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")  # type: ignore

# Inicializar cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) # type: ignore

def main():
    """Configura e inicia el bot"""
    # Crear la aplicación
    app = Application.builder().token(TELEGRAM_TOKEN).build() # type: ignore

    # Añadir manejadores de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("novels", get_novels))

    print("Bot en marcha... Presiona Ctrl+C para detenerlo.")
    app.run_polling()

if __name__ == "__main__":
    main()