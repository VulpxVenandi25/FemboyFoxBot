from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .config import ITEMS_PER_PAGE
from .novels import NOVELS_LIST, get_page

def build_novels_keyboard(page):
    keyboard = []
    novels_page = get_page(page)

    for novel in novels_page:
        keyboard.append([InlineKeyboardButton(novel["name"], callback_data=f"novel_{novel['gameid']}")])

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"page_{page-1}"))
    if (page + 1) * ITEMS_PER_PAGE < len(NOVELS_LIST):
        pagination_buttons.append(InlineKeyboardButton("Siguiente ➡️", callback_data=f"page_{page+1}"))

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    return InlineKeyboardMarkup(keyboard)

def build_back_to_list_keyboard(page=0):
    keyboard = [[InlineKeyboardButton("🔙 Volver a la lista", callback_data=f"back_to_list_{page}")]]
    return InlineKeyboardMarkup(keyboard)
