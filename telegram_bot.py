cat > telegram_bot.py <<'PY'
import requests, json, os

CFG_PATH = "/app/config.json" if os.path.exists("/app/config.json") else "./config.json"
with open(CFG_PATH) as f:
    cfg = json.load(f)

TOKEN = cfg.get("telegram", {}).get("bot_token")
CHAT_ID = cfg.get("telegram", {}).get("chat_id")

def send_message(text):
    if not TOKEN or not CHAT_ID:
        print("Telegram non configurato in config.json")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            print("Telegram error:", resp.status_code, resp.text)
    except Exception as e:
        print("Errore invio Telegram:", e)

if __name__ == "__main__":
    send_message("SmartDoctor: test Telegram (script telegram_bot.py)")
PY
