import os
import requests

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = os.environ["DISCORD_CHANNEL_ID"]

URL = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "content": (
        "🧪 **TEST NTE CODE BOT**\n\n"
        "Si tu vois ce message, la connexion Discord fonctionne !\n\n"
        "🔑 `TEST-NTE-CODE`\n\n"
        "📋 Le code peut être copié directement depuis Discord."
    )
}

response = requests.post(
    URL,
    headers=headers,
    json=data,
    timeout=20
)

if response.status_code == 200:
    print("✅ Message envoyé avec succès sur Discord !")
else:
    print(f"❌ Erreur Discord : {response.status_code}")
    print(response.text)
    response.raise_for_status()
