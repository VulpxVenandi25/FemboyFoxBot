from telegram.ext import ApplicationBuilder, CallbackQueryHandler ,CommandHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import json, requests, os

load_dotenv()
api_token = os.environ.get("API_TOKEN")
itch_token = os.environ.get("ITCH_TOKEN")

commands = [
    {"command": "/help", "description": "Ofrece una ayuda más detallada."},
    {"command": "/novels", "description": "Da una lista de todas las novelas traducidas."}
]

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.name
    await update.message.reply_html(f"""
Hola {name}, soy femboyFoxBot y soy el encargado de compartir las novelas visuales traducidas al español qué mi creador, @VulpVenandi25 traduzca.

Puedes seguir sus redes sociales desde este <a href="https://linktr.ee/vulpxvenandi25">link</a>, o usar el comando /help para más información.
""")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_text = "\n".join([f'🔰 {com["command"]}: {com["description"]}' for com in commands])
    await update.message.reply_html(f"""
Encantado de ayudar, los comando disponibles por ahora son los siguientes:

{commands_text}
""")
    return

# Cargar datos de novelas traducidas
with open('json/allTranslated.json', 'r', encoding='utf-8') as f:
    novels_data = json.load(f)

# Configuración
ITEMS_PER_PAGE = 10
NOVELS_LIST = novels_data["allTranslated"]

async def novels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra la primera página de novelas con botones de paginación"""
    await show_novels_page(update, context, page=0)

async def show_novels_page(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int):
    """Muestra una página específica de la lista de novelas"""
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    novels_page = NOVELS_LIST[start_idx:end_idx]
    
    # Crear teclado inline
    keyboard = []
    
    # Botones para cada novela
    for novel in novels_page:
        keyboard.append([InlineKeyboardButton(novel["name"], callback_data=f"novel_{novel['gameid']}")])
    
    # Botones de paginación
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"page_{page-1}"))
    if end_idx < len(NOVELS_LIST):
        pagination_buttons.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"page_{page+1}"))
    
    if pagination_buttons:
        keyboard.append(pagination_buttons)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Enviar mensaje
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text=f"📚 Novelas traducidas (página {page+1}):",
                reply_markup=reply_markup
            )
        except Exception as e:
            # Si falla editar el texto (porque el mensaje es una foto), enviar un nuevo mensaje
            await update.callback_query.message.reply_text(
                text=f"📚 Novelas traducidas (página {page+1}):",
                reply_markup=reply_markup
            )
            # Opcional: eliminar el mensaje anterior
            await update.callback_query.delete_message()
    else:
        await update.message.reply_text(
            text=f"📚 Novelas traducidas (página {page+1}):",
            reply_markup=reply_markup
        )

async def show_novel_details(update: Update, context: ContextTypes.DEFAULT_TYPE, gameid: str):
    """Muestra los detalles de una novela específica"""
    # Obtener datos de la API
    api_url = f"https://itch.io/api/1/{itch_token}/game/{gameid}"

    response = requests.get(api_url)
    
    if response.status_code != 200:
        await update.callback_query.answer("Error al obtener los detalles de la novela")
        return
    
    game_data = response.json()["game"]
    
    # Buscar la novela en nuestra lista para obtener el link
    novel_info = next((n for n in NOVELS_LIST if n["gameid"] == gameid), None)
    
    if not novel_info:
        await update.callback_query.answer("Novela no encontrada")
        return
    
    # Formatear mensaje con los detalles
    message_parts = [
        f"📖 <b>{game_data['title']}</b>\n\n"
    ]

    if game_data.get('short_text'):
        message_parts.append(f"🔹 <i>{game_data['short_text']}</i>\n\n")
    
    if game_data.get('user', {}).get('display_name'):
        message_parts.append(f"👤 <b>Autor:</b> {game_data['user']['display_name']}\n")

    message_parts.extend([
        f"🌐 <b>Página oficial:</b> {novel_info['link']}\n",
        f"📅 <b>Publicado:</b> {game_data['published_at'].split('T')[0]}\n",
        f"💰 <b>Precio mínimo:</b> ${game_data['min_price'] if game_data.get('min_price') is not None else 'Gratis'}\n\n"
        "<b>Descargalo desde el siguiente enlace de <a href='https://1024terabox.com/s/1BH1epgCdYnn-yFWZHqtcSw'>Terabox</a></b>\n"
        "<i><b>Nota:</b> Necesitas una cuenta para poder descargarlo.</i>"
    ])

    message = ''.join(message_parts)
    
    keyboard = [
        [InlineKeyboardButton("🔙 Volver a la lista", callback_data=f"back_to_list_0")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        # Primero editar el mensaje existente a texto plano
        await update.callback_query.edit_message_text(
            text="Cargando detalles...",
            reply_markup=None
        )
        
        if game_data.get('cover_url'):
            # Enviar la foto como nuevo mensaje
            await update.callback_query.message.reply_photo(
                photo=game_data['cover_url'],
                caption=message,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            # Eliminar el mensaje anterior
            await update.callback_query.delete_message()
        else:
            # Si no hay foto, editar el mensaje con los detalles
            await update.callback_query.edit_message_text(
                text=message,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"Error al mostrar detalles: {e}")
        # Si falla todo, enviar un nuevo mensaje
        await update.callback_query.message.reply_text(
            text=message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador de callbacks para los botones inline"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith("page_"):
        # Navegación entre páginas
        page = int(data.split("_")[1])
        await show_novels_page(update, context, page)
    elif data.startswith("novel_"):
        # Mostrar detalles de una novela
        gameid = data.split("_")[1]
        await show_novel_details(update, context, gameid)
    elif data.startswith("back_to_list_"):
        try:
            page = int(data[len("back_to_list_"):])  # extrae directamente el número después del prefijo
        except ValueError:
            page = 0  # valor por defecto si algo sale mal
        await show_novels_page(update, context, page)
    
application = ApplicationBuilder().token(api_token).build()

application.add_handler(CommandHandler("start", say_hello))
application.add_handler(CommandHandler("help", help))
application.add_handler(CommandHandler("novels", novels))
application.add_handler(CallbackQueryHandler(handle_callback))

application.run_polling(allowed_updates=Update.ALL_TYPES)