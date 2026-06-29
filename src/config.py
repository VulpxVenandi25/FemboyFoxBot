from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ITCH_TOKEN = os.environ.get("ITCH_TOKEN")
ITEMS_PER_PAGE = 10
ITCH_API_URL = "https://itch.io/api/1"
NOVELS_API_URL = "https://vv25-backend.vercel.app/api/novel"
