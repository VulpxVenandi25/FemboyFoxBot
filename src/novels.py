import requests
from .config import ITCH_TOKEN, ITCH_API_URL, NOVELS_API_URL, ITEMS_PER_PAGE

response = requests.get(NOVELS_API_URL)
response.raise_for_status()
NOVELS_LIST = [{"gameid": str(n["id"]), "name": n["name"], "link": n["link"]} for n in response.json()]

def get_page(page):
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    return NOVELS_LIST[start:end]

def get_novel_by_gameid(gameid):
    return next((n for n in NOVELS_LIST if n["gameid"] == gameid), None)

def fetch_novel_details(gameid):
    url = f"{ITCH_API_URL}/{ITCH_TOKEN}/game/{gameid}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()["game"]
