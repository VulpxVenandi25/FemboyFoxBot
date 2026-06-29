import io
import csv
from telegram import Update
from telegram.ext import ContextTypes
from .novels import NOVELS_LIST, fetch_novel_details, get_novel_by_gameid
from .keyboards import build_novels_keyboard, build_back_to_list_keyboard

commands = [
    {"command": "/help", "description": "Ofrece una ayuda más detallada."},
    {"command": "/novels", "description": "Da una lista de todas las novelas traducidas."},
    {"command": "/poll", "description": "Crea una encuesta: /poll \"Pregunta\" \"Op1\" \"Op2\" ..."}
]

user_polls = {}

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.name
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

async def novels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_novels_page(update, context, page=0)

async def show_novels_page(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int):
    reply_markup = build_novels_keyboard(page)

    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text=f"📚 Novelas traducidas (página {page+1}):",
                reply_markup=reply_markup
            )
        except Exception:
            await update.callback_query.message.reply_text(
                text=f"📚 Novelas traducidas (página {page+1}):",
                reply_markup=reply_markup
            )
            await update.callback_query.delete_message()
    else:
        await update.message.reply_text(
            text=f"📚 Novelas traducidas (página {page+1}):",
            reply_markup=reply_markup
        )

async def show_novel_details(update: Update, context: ContextTypes.DEFAULT_TYPE, gameid: str):
    game_data = fetch_novel_details(gameid)

    if not game_data:
        await update.callback_query.answer("Error al obtener los detalles de la novela")
        return

    novel_info = get_novel_by_gameid(gameid)
    if not novel_info:
        await update.callback_query.answer("Novela no encontrada")
        return

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
        "<b>Descargalo desde el siguiente enlace de <a href='https://1024terabox.com/s/1tE9OQQX52AbNFlxX3Wohvg'>Terabox</a></b>\n"
        "<i><b>Nota:</b> Necesitas una cuenta para poder descargarlo.</i>"
    ])
    message = ''.join(message_parts)
    reply_markup = build_back_to_list_keyboard()

    try:
        await update.callback_query.edit_message_text(text="Cargando detalles...", reply_markup=None)
        if game_data.get('cover_url'):
            await update.callback_query.message.reply_photo(
                photo=game_data['cover_url'],
                caption=message,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            await update.callback_query.delete_message()
        else:
            await update.callback_query.edit_message_text(
                text=message, parse_mode='HTML', reply_markup=reply_markup
            )
    except Exception as e:
        print(f"Error al mostrar detalles: {e}")
        await update.callback_query.message.reply_text(
            text=message, parse_mode='HTML', reply_markup=reply_markup
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("page_"):
        page = int(data.split("_")[1])
        await show_novels_page(update, context, page)
    elif data.startswith("novel_"):
        gameid = data.split("_")[1]
        await show_novel_details(update, context, gameid)
    elif data.startswith("back_to_list_"):
        try:
            page = int(data[len("back_to_list_"):])
        except ValueError:
            page = 0
        await show_novels_page(update, context, page)

async def create_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_html(
            "<b>Uso:</b> /poll \"Pregunta\" \"Opción 1\" \"Opción 2\" ...\n\n"
            "<b>Ejemplo:</b>\n"
            "<code>/poll \"Cuál prefieres?\" \"Fuego\" \"Agua\" \"Hierba\"</code>"
        )
        return

    question = args[0]
    options = args[1:]

    if len(options) > 10:
        await update.message.reply_text("Máximo 10 opciones.")
        return

    msg = await update.message.reply_poll(
        question=question,
        options=options,
        is_anonymous=False,
    )

    user_polls[msg.poll.id] = {
        "question": question,
        "chat_id": update.effective_chat.id,
    }

async def track_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poll = update.poll
    if poll.id not in user_polls:
        return
    if not poll.is_closed:
        return

    info = user_polls[poll.id]
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Opción", "Votos"])
    for opt in poll.options:
        writer.writerow([opt.text, opt.voter_count])

    await context.bot.send_document(
        chat_id=info["chat_id"],
        document=io.BytesIO(output.getvalue().encode("utf-8-sig")),
        filename="encuesta.csv",
        caption=f"Resultados finales: {poll.question}"
    )

    del user_polls[poll.id]

async def handle_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    poll = update.message.poll
    total_votes = sum(opt.voter_count for opt in poll.options)

    if total_votes == 0:
        await update.message.reply_text(
            "Las encuestas reenviadas no incluyen los votos "
            "(límite de Telegram). Usá /poll para crear una "
            "encuesta directamente desde el bot."
        )
        return

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Opción", "Votos"])
    for option in poll.options:
        writer.writerow([option.text, option.voter_count])
    await update.message.reply_document(
        document=io.BytesIO(output.getvalue().encode("utf-8-sig")),
        filename="encuesta.csv",
        caption=f"Resultados de la encuesta: {poll.question}"
    )
