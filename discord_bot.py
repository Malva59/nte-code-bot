import os
import requests


DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = os.environ["DISCORD_CHANNEL_ID"]

ROLE_ID = "1543027793695088640"

DISCORD_URL = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"


def send_code(code):
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "content": f"<@&{ROLE_ID}>",
        "allowed_mentions": {
            "roles": [ROLE_ID]
        },
        "embeds": [
            {
                "title": "🎁 NOUVEAU CODE NTE !",
                "description": (
                    "Un nouveau code pour **Neverness to Everness** "
                    "vient d'être détecté !"
                ),
                "fields": [
                    {
                        "name": "🔑 Code",
                        "value": f"```{code}```",
                        "inline": False
                    },
                    {
                        "name": "🎁 Récompenses",
                        "value": "Récompenses disponibles en jeu.",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "NTE Code Bot • Source : NTEBuild"
                }
            }
        ]
    }

    response = requests.post(
        DISCORD_URL,
        headers=headers,
        json=data,
        timeout=20
    )

    response.raise_for_status()

    print(f"[DISCORD] Code envoyé : {code}")
