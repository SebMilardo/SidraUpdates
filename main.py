import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://sidraspa.it/area-comunicazione/interventi-sulla-rete/"
STATE_FILE = "last.json"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": True,
        },
        timeout=20,
    )


def fetch_notices():
    r = requests.get(URL, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    notices = []

    for article in soup.find_all("article"):
        title_tag = article.find(["h2", "h3", "h4", "h5"])
        link_tag = article.find("a")

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)

        link = None
        if link_tag and link_tag.get("href"):
            link = link_tag["href"]

        notices.append({
            "title": title,
            "link": link
        })

    return notices


def main():
    state = load_state()
    seen = set(state.get("seen", []))

    notices = fetch_notices()

    new_notices = []

    for notice in notices:
        if notice["title"] not in seen:
            new_notices.append(notice)

    if new_notices:
        for notice in reversed(new_notices):

            message = f"🚰 Nuovo intervento SIDRA\n\n{notice['title']}\n\n{URL}"

            send_telegram(message)

            seen.add(notice["title"])

        save_state({"seen": list(seen)})

        print(f"Nuovi avvisi trovati: {len(new_notices)}")

    else:
        print("Nessun nuovo avviso")


if __name__ == "__main__":
    main()
