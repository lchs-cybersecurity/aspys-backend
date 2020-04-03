from datetime import datetime, timedelta
import pytz
import requests
from json import load as json_load

def now():
    return datetime.now(pytz.utc)

def limit_str(str, chars):
    return str[:chars-3] + (str[chars-3:] and "...")

def tryDiscordSend(data):
    try:
        with open("config.json", "r") as config_file:
            config = json_load(config_file)
        if "discord_webhook" in config and data:
            discord_webhook = config['discord_webhook']
            embed_fields = []
            for field in data['fields']:
                embed_fields.append({
                    "name":limit_str(field["label"], 256),
                    "value":limit_str(field["value"], 1024)
                })
            message = {
                "embeds": [{
                    "color": data['color'] if 'color' in data else "53622",
                    "title": data['title'] if 'title' in data else "Veritas",
                    "timestamp": str(now()),
                    "fields": embed_fields
                }]
            }
            response = requests.post(discord_webhook, json=message)
            return response
        return False
    except Exception as e:
        print(f"Exception: {e}")
        return e