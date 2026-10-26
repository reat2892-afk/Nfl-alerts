import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def main():
    if not BOT_TOKEN or not CHAT_ID:
        print("Faltan secrets TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID")
        return

    mensaje = "🏈 ¡Bot de Alertas de la 【entity-NFL¦canonical_name=NFL】 activo!\n\n✅ Tu bot ya está funcionando correctamente en GitHub Actions.\n\nAhora ya puedes recibir alertas de juegos, lesiones y apuestas."

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mensaje}
    
    r = requests.post(url, json=data)
    print(f"Respuesta Telegram: {r.text}")
    if r.status_code == 200:
        print("¡Mensaje enviado a Telegram!")
    else:
        print(f"Error: {r.text}")

if __name__ == "__main__":
    main()
