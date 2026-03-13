import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
load_dotenv()

URL = "https://sidraspa.it/area-comunicazione/interventi-sulla-rete/"
BASE = "https://sidraspa.it"

STATE_FILE = "last.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": msg,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )


def fetch_notices():
    r = requests.get(URL, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    notices = []

    cards = soup.select("div.card")

    for card in cards:

        title_tag = card.select_one("h5.card-title a")
        date_tag = card.select_one("span.data")
        text_tag = card.select_one("p.card-text")

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = BASE + title_tag["href"]
        date = date_tag.get_text(strip=True) if date_tag else ""
        text = text_tag.get_text(strip=True)[:300] if text_tag else ""

        notices.append({
            "id": link,
            "title": title,
            "date": date,
            "text": text,
            "link": link
        })

    return notices


def main():
    state = load_state()
    seen = set(state.get("seen", []))

    notices = fetch_notices()

    new_notices = [n for n in notices if n["id"] not in seen]

    if new_notices:

        for notice in reversed(new_notices):

            message = (
                f"🚰 Nuovo intervento SIDRA\n\n"
                f"{notice['title']}\n"
                f"{notice['date']}\n\n"
                f"{notice['text']}...\n\n"
                f"{notice['link']}"
            )

            send_telegram(message)

            seen.add(notice["id"])

        save_state({"seen": list(seen)})

        print(f"Nuovi avvisi trovati: {len(new_notices)}")

    else:
        print("Nessun nuovo avviso")


if __name__ == "__main__":
    main()