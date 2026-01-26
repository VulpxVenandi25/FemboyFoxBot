from telegram import Update
from telegram.ext import ContextTypes
from model.Supabase import supabase

async def get_novels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Consulta la base de datos y lista las novelas"""
    try:
        # Consultamos la tabla 'novelas'
        response = supabase.table("novel").select("name").execute()
        data = response.data

        if not data:
            await update.message.reply_text("No hay novelas registradas por ahora.") # type: ignore
            return

        # Formateamos la lista
        mensaje = "📚 **Lista de Novelas:**\n\n"
        for i, novela in enumerate(data, 1):
            mensaje += f"{i}. {novela['name']}\n" # type: ignore

        await update.message.reply_text(mensaje, parse_mode="Markdown") # type: ignore

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Hubo un error al conectar con la base de datos.") # type: ignore