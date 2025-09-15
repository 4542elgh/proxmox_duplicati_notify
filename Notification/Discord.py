from Notification.MessageService import MessageService
from dataclasses import dataclass

@dataclass
class Embed:
    title: str = ""
    url: str = ""
    description: str = ""
    color: int = 0

@dataclass
class Discord(MessageService):
    """
    Concrete notification service for Discord webhooks.

    Uses Discord embeds to send messages with optional severity coloring.

    Args:
        duplicati_url (str): The URL of the Duplicati backup service.
        webhook_url (str): The Discord webhook endpoint.
        headers (dict): HTTP headers for the request (e.g., Content-Type).
    """
    _embeds: list[Embed]

    def __init__(self, duplicati_url:str, webhook_url:str, headers:dict = {}) -> None:
        self._embeds = [Embed(title="Duplicati", url=duplicati_url)]
        self._webhook_url = webhook_url
        self._headers = headers

    @property
    def body(self) -> str:
        return self._embeds[0].description

    @body.setter
    def body(self, body:str) -> None:
        self._embeds[0].description = body

    @property
    def duplicati_url(self) -> str:
        return self._embeds[0].url

    @duplicati_url.setter
    def duplicati_url(self, duplicati_url:str) -> None:
        self._embeds[0].url = duplicati_url

    @property
    def severity(self) -> int:
        return self._embeds[0].color

    @severity.setter
    def severity(self, severity) -> None:
        self._embeds[0].color = 16711680 if severity == "error" else 65280
    
    def as_dict(self) -> dict:
        embed:Embed = self._embeds[0]
        return {
            "embeds": [
                {
                    "title": embed.title,
                    "url": embed.url,
                    "description": embed.description,
                    "color": embed.color
                }
            ]
        }