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
    name = update.message.from_user.full_name
    await update.message.reply_html(f"""
Hola {name}, soy femboyFoxBot y soy el encargado de compartir las novelas visuales traducidas al español qué mi creador, @VulpVenandi25 traduzca.

Puedes seguir sus redes sociales desde este <a href="https://linktr.ee/vulpxvenandi25">link</a>, o usar el comando /help para más información.
""")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_text = "\n".join([f'🔰 {com["command"]}: {com["description"]}' for com in commands])
    await update.message.reply_html(f"""
Encantado de ayudar, los comando disponibles por ahora son los siguientes:

{commands_text}
""")
    return

# Cargar datos de novelas traducidas desde la API
novels_data = []
try:
    response = requests.get("https://backend-vv25.vercel.app/api/novels")
    response.raise_for_status()
    novels_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error en la petición HTTP: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")

# Configuración
ITEMS_PER_PAGE = 10
NOVELS_LIST = novels_data


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
        keyboard.append([InlineKeyboardButton(novel["name"], callback_data=f"novel_{novel['id']}")])
    
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
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

async def show_novel_details(update: Update, context: ContextTypes.DEFAULT_TYPE, id: str):
    """Muestra los detalles de una novela específica"""
    api_url = f"https://backend-vv25.vercel.app/api/apigame/{id}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        game_data = response.json()
        
        # Buscar la novela en nuestra lista para obtener el link
        novel_info = next((n for n in NOVELS_LIST if n["id"] == int(id)), None)
        ##novel_info = next((n for n in NOVELS_LIST if n["id"] == id), None)
        
        if not novel_info:
            await update.callback_query.answer("Novela no encontrada")
            return
        
        # # Formatear mensaje con los detalles
        message_parts = []

        # Obtener el objeto game del JSON (si existe)
        game_info = game_data.get('game', {}) if isinstance(game_data, dict) else {}

        # Título del juego
        if game_info.get('title'):
            message_parts.append(f"📖 <b>{game_info['title']}</b>\n\n")

        # Descripción corta
        if game_info.get('short_text'):
            message_parts.append(f"🔹 <i>{game_info['short_text']}</i>\n\n")

        # Información del autor
        if game_info.get('user', {}).get('display_name'):
            user_info = game_info['user']
            author_line = f"👤 <b>Autor:</b> {user_info['display_name']}"
            if user_info.get('url'):
                author_line += f" (<a href='{user_info['url']}'>itch.io</a>)"
            message_parts.append(f"{author_line}\n")

        # Información básica del juego
        info_lines = [
            f"🌐 <b>Página oficial:</b> {novel_info.get('link', game_info.get('url', 'No disponible'))}\n",
            f"📅 <b>Publicado:</b> {game_info.get('published_at', '').split('T')[0]}\n",
            f"💰 <b>Precio mínimo:</b> ${game_info.get('min_price', 0) if game_info.get('min_price') is not None else 'Gratis'}\n\n"
        ]

        # Plataformas disponibles (si existen)
        platforms = {
            'p_windows': 'Windows',
            'p_linux': 'Linux',
            'p_osx': 'macOS',
            'p_android': 'Android'
        }

        available_platforms = [
            platforms[trait] 
            for trait in game_info.get('traits', []) 
            if trait in platforms
        ]

        if available_platforms:
            info_lines.append(f"🖥️ <b>Plataformas:</b> {', '.join(available_platforms)}\n")

        message_parts.extend(info_lines)

        # Información de descarga
        message_parts.extend([
            "<b>Descárgalo desde:</b>\n",
            "🔗 <a href='https://1024terabox.com/s/1BH1epgCdYnn-yFWZHqtcSw'>Terabox</a>\n",
            "<i>Nota: Necesitas una cuenta para poder descargarlo.</i>"
        ])

        # Unir todas las partes del mensaje

        message = ''.join(message_parts)
        
        keyboard = [
            [InlineKeyboardButton("🔙 Volver a la lista", callback_data=f"back_to_list_0")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Intentar mostrar la imagen de portada si existe
        if game_info.get('cover_url'):
            cover_url = game_info.get('cover_url') or game_data.get('cover_image')
        
        if cover_url:
            try:
                await update.callback_query.message.reply_photo(
                    photo=cover_url,
                    caption=message,
                    parse_mode='HTML',
                    reply_markup=reply_markup
                )
                await update.callback_query.delete_message()
                return
            except Exception as e:
                print(f"Error al enviar foto: {e}")
        
        # Si no hay foto o falló el envío, enviar solo texto
        await update.callback_query.edit_message_text(
            text=message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )

    except requests.exceptions.RequestException as e:
        print(f"Error en la petición HTTP: {e}")
        await update.callback_query.answer("Error al conectar con el servidor")
    except Exception as e:
        print(f"Error inesperado: {e}")
        await update.callback_query.answer("Ocurrió un error al mostrar los detalles")

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
        id = data.split("_", 1)[1]
        await show_novel_details(update, context, id)
    elif data.startswith("back_to_list_"):
        try:
            page = int(data[len("back_to_list_"):])  # extrae directamente el número después del prefijo
        except ValueError:
            page = 0  # valor por defecto si algo sale mal
        await show_novels_page(update, context, page)
    
application = ApplicationBuilder().token(api_token).build()

application.add_handler(CommandHandler("start", say_hello))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("novels", novels))
application.add_handler(CallbackQueryHandler(handle_callback))

## application.run_polling(allowed_updates=Update.ALL_TYPES)
application.run_polling()