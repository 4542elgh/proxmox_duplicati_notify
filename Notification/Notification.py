import logging
import requests
from Notification.Apprise import Apprise
from Notification.Discord import Discord
from Notification.NotificationEnum import NOTIFICATION

# Made messaging service more modular
class Notification:
    """
    Notification service utility class.

    This module provides a `Notification` class that initializes and sends
    messages through different notification backends (Apprise/Discord).
    It validates the service type, constructs the appropriate payload, and handles
    delivery via HTTP requests.

    Supported Services:
        - Apprise: A notification service that supports multiple platforms.
        - Discord: Sends messages to a Discord channel using a webhook URL.
    """
    def __init__(self, notification_service:str, webhook_url:str, tag:str, duplicati_url:str) -> None:
        self.logger: logging.Logger = logging.getLogger()
        self.headers: dict = {}

        notification_service = notification_service.strip().lower()

        if (notification_service in [e.value for e in NOTIFICATION] and webhook_url.strip()):
            if (notification_service == NOTIFICATION.APPRISE.value):
                self.service_type = NOTIFICATION.APPRISE
                self.payload = Apprise(tag=tag, duplicati_url=duplicati_url, webhook_url=webhook_url)
            elif (notification_service == NOTIFICATION.DISCORD.value):
                self.service_type = NOTIFICATION.DISCORD
                self.payload = Discord(duplicati_url=duplicati_url, webhook_url=webhook_url, headers={ "Content-Type": "application/json" })
        else:
            raise ValueError(f"Notification service is not one of the accepted values: {[e.value for e in NOTIFICATION]}")
    
    # Severity only available for discord webhook (using embeds)
    def send(self, msg:str, severity:str = "") -> None:
        if (self.payload is not None):
            self.payload.body = msg
            if isinstance(self.payload, Discord):
                self.payload.severity = severity
            
            try:
                response = requests.post(
                                url = self.payload.webhook_url,
                                json = self.payload.as_dict(),
                                timeout = 10,
                                headers = self.headers)
                response.raise_for_status()
            except requests.RequestException as e:
                self.logger.error("Failed to send notification: %s", e)