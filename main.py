import threading
from src.bot import BotApp
from src.ui import BotUI

def main():
    bot_app = BotApp()
    bot_app.setup()

    ui = BotUI(bot_app)

    bot_thread = threading.Thread(target=bot_app.run, daemon=True)
    bot_thread.start()

    ui.run()

if __name__ == "__main__":
    main()
