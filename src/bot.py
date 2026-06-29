from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, PollHandler, filters
from .config import TELEGRAM_TOKEN
from .handlers import say_hello, help_command, novels, handle_callback, handle_poll, create_poll, track_poll

class BotApp:
    def __init__(self):
        self.application = None
        self.is_running = False
        self.start_time = None
        self.last_interaction = None
        self.events = []

    def setup(self):
        self.application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        self.application.add_handler(CommandHandler("start", say_hello))
        self.application.add_handler(CommandHandler("help", help_command))
        self.application.add_handler(CommandHandler("novels", novels))
        self.application.add_handler(CommandHandler("poll", create_poll))
        self.application.add_handler(MessageHandler(filters.POLL, handle_poll))
        self.application.add_handler(PollHandler(track_poll))
        self.application.add_handler(CallbackQueryHandler(handle_callback))

    def run(self):
        self.is_running = True
        self.start_time = datetime.now()
        self.add_event("Bot iniciado")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def stop(self):
        if self.application:
            self.application.stop()
        self.is_running = False
        self.add_event("Bot detenido")

    def add_event(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.events.append(f"[{timestamp}] {msg}")
        if len(self.events) > 100:
            self.events.pop(0)

    def get_info(self):
        uptime = ""
        if self.start_time:
            uptime = str(datetime.now() - self.start_time).split('.')[0]
        return {
            "running": self.is_running,
            "uptime": uptime,
            "last_interaction": self.last_interaction or "Ninguna",
            "events": list(self.events)
        }
