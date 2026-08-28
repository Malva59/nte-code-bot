import os
import requests


DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = os.environ["DISCORD_CHANNEL_ID"]

DISCORD_URL = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"


def send_code(code):
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "embeds": [
            {
                "title": "🎁 NOUVEAU CODE NTE !",
                "description": (
                    "Un nouveau code pour **Neverness to Everness** vient d'être détecté !"
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
                    },
                    {
                        "name": "⚡ Statut",
                        "value": "🟢 Code actif",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "NTE Code Bot • Source : NTEBuild"
                }
            }
        ],
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "style": 5,
                        "label": "❓ Comment utiliser",
                        "url": "https://www.ntebuild.com/codes"
                    }
                ]
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

    # Message séparé sous l'embed pour faciliter la copie
    copy_data = {
        "content": f"📋 **Code à copier :**\n```{code}```"
    }

    response = requests.post(
        DISCORD_URL,
        headers=headers,
        json=copy_data,
        timeout=20
    )

    response.raise_for_status()

    print(f"[DISCORD] Code envoyé : {code}")
