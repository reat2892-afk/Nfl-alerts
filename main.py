import os
import requests
import asyncio
from datetime import datetime

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ODDS_KEY = os.getenv("ODDS_API_KEY")

async def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(e)

def revisar_liga(sport_key, nombre_liga):
    if not ODDS_KEY:
        return []
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
    params = {
        "apiKey": ODDS_KEY,
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "american",
        "bookmakers": "caliente,bet365,betano"
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code != 200:
            print(f"{nombre_liga} error: {r.status_code}")
            return []
        data = r.json()
        traps = []
        for juego in data[:5]:
            partido = f"{juego['away_team']} @ {juego['home_team']}"
            momios = {}
            for book in juego.get('bookmakers', []):
                key = book['key']
                for market in book['markets']:
                    if market['key'] == 'h2h':
                        for out in market['outcomes']:
                            k = out['name']
                            momios.setdefault(k, {})[key] = out['price']
            for equipo, casas in momios.items():
                if 'caliente' in casas:
                    for otra, odd_otra in casas.items():
                        if otra == 'caliente': continue
                        diff = abs(casas['caliente'] - odd_otra)
                        if diff >= 20:
                            traps.append({"liga": nombre_liga, "partido": partido, "equipo": equipo, "caliente": casas['caliente'], "otra_casa": otra, "otra_odd": odd_otra, "diff": diff})
        return traps
    except Exception as e:
        print(f"Error {nombre_liga}: {e}")
        return []

async def main():
    print(f"Iniciando NFL + Liga MX {datetime.now()}")
    todos_traps = []
    todos_traps += revisar_liga("americanfootball_nfl", "NFL")
    todos_traps += revisar_liga("soccer_mexico_ligamx", "Liga MX")
    if todos_traps:
        for t in todos_traps:
            msg = f"🚨 *TRAP {t['liga']}*\n🏈 {t['partido']}\n🎯 {t['equipo']}\n💰 Caliente: {t['caliente']}\n💰 {t['otra_casa']}: {t['otra_odd']}\n📊 Diff: {t['diff']}"
            await send_telegram(msg)
    else:
        await send_telegram(f"✅ Bot NFL + Liga MX {datetime.now().strftime('%H:%M')} - Sin traps >20pts")

if __name__ == "__main__":
    import asyncio as _a
    _a.run(main())
