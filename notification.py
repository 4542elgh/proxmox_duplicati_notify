import logging
import requests
from enum import Enum

class NOTIFICATION(Enum):
    APPRISE = "apprise"
    DISCORD = "discord"

class Notification:
    def __init__(self, notification_service:str, webhook_url:str, tag:str, duplicati_url:str) -> None:
        self.logger = logging.getLogger()
        self.tag = tag
        self.duplicati_url = duplicati_url
        self.headers = {}

        notification_service = notification_service.strip().lower()
        if (notification_service in [e.value for e in NOTIFICATION] and webhook_url.strip()):
            self.url = webhook_url
            if (notification_service == NOTIFICATION.APPRISE.value):
                self.service_type = NOTIFICATION.APPRISE
            elif (notification_service == NOTIFICATION.DISCORD.value):
                self.service_type = NOTIFICATION.DISCORD
                self.headers = {
                    "Content-Type": "application/json"
                }
        else:
            raise ValueError(f"Notification service is not one of the accepted values: {[e.value for e in NOTIFICATION]}")
    
    # Severity only available for discord webhook (using embeds)
    def send(self, msg:str, severity:str = "") -> None:
        json = {}
        if (self.service_type == NOTIFICATION.APPRISE):
            json["body"] = msg + ("\n" + self.duplicati_url) if self.duplicati_url else ""
            json["tag"] = self.tag
        else:
            json = {
                "embeds": [
                    {
                        "title": "Duplicati",
                        "url": self.duplicati_url if self.duplicati_url else "",
                        "description": msg,
                        "color": 16711680 if severity == "error" else 65280
                    }
                ]
            }
        
        try:
            response = requests.post(
                            url = self.url,
                            json = json,
                            timeout = 10,
                            headers = self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error("Failed to send notification: %s", e)