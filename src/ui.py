import os
import webview
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GUI_DIR = BASE_DIR / "gui"


class BotAPI:
    def __init__(self, bot_app):
        self._bot_app = bot_app

    def get_info(self):
        return self._bot_app.get_info()


class BotUI:
    def __init__(self, bot_app):
        self.bot_app = bot_app
        self.window = None
        self.api = BotAPI(self.bot_app)

    def run(self):
        index_path = (GUI_DIR / "index.html").as_uri()
        self.window = webview.create_window(
            "FemboyFoxBot - Panel de Control",
            url=index_path,
            js_api=self.api,
            width=420,
            height=480,
            resizable=False
        )
        webview.start()
