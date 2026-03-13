# SidraUpdates

A lightweight Python script that monitors the SIDRA Spa “interventi sulla rete” updates page and sends new notices to a Telegram chat.

---

## ✅ What it does

- Scrapes https://sidraspa.it/area-comunicazione/interventi-sulla-rete/
- Detects new notices (interventi) that haven't been seen before
- Sends a Telegram message for each new notice
- Persists seen notices in `last.json` to avoid duplicates

---

## 🚀 Quick Start

### 1) Clone the repo

```bash
git clone <repo-url>
cd SidraUpdates
```

### 2) Install dependencies

```bash
python -m pip install -r requirements.txt
```

Or with `pyproject.toml`:

```bash
python -m pip install .
```

### 3) Configure environment variables

Create a `.env` file in the project root with:

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
CHAT_ID=-1001234567890
```

- `BOT_TOKEN`: your Telegram bot token
- `CHAT_ID`: your Telegram chat id (group/channel or direct chat)

### 4) Run the script

```bash
python main.py
```

---

## 🧠 How it works

- `main.py` fetches the list of notices from SIDRA's public page.
- It extracts the title, date, snippet, and link from each card.
- Notices are deduped using `last.json` (stored as a list of seen notice URLs).
- New notices are sent through the Telegram Bot API.

---

## 🔧 Customization

- Change `URL`/`BASE` in `main.py` if the source page changes.
- Update the message formatting inside `main.py`.

---

## 🕒 Scheduling (Optional)

Run the script periodically using cron (Linux/macOS) or a scheduled task.

Example cron job (every 10 minutes):

```cron
*/10 * * * * cd /path/to/SidraUpdates && python main.py >> /path/to/SidraUpdates/sidra.log 2>&1
```

---

## 🧪 Troubleshooting

- If you don’t get messages, ensure `BOT_TOKEN` and `CHAT_ID` are correct.
- If the script can’t fetch the page, verify your network and that `sidraspa.it` is reachable.

---

## 📦 Dependencies

Defined in `pyproject.toml`:

- `beautifulsoup4`
- `python-dotenv`
- `python-telegram-bot`
- `requests`

---

## 📝 Notes

- By default, the script uses the Telegram Bot API via `requests` rather than `python-telegram-bot`.
- `last.json` is created in the project root and stores seen notice URLs.
