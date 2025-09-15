from Notification.MessageService import MessageService
from dataclasses import dataclass

# Abstract class, this is a foundation/bare minimum a class inheriting this class needs to supply
@dataclass
class Apprise(MessageService):
    """
    Concrete notification service for Apprise.

    Implements the `MessageService` interface to build a payload suitable
    for Apprise, including message content, a notification tag, and an
    optional Duplicati URL.

    Args:
        tag (str): Tag used to filter notification targets in Apprise.
        duplicati_url (str): URL of the Duplicati backup service (optional).
        webhook_url (str): The Apprise webhook endpoint.
        headers (dict, optional): Optional HTTP headers for the request.
    """
    _body:str = ""
    _duplicati_url:str = ""
    _tag:str = ""

    def __init__(self, tag:str, duplicati_url:str, webhook_url:str, headers: dict = {}) -> None:
        self._duplicati_url = duplicati_url
        self._webhook_url = webhook_url
        self._tag = tag
        self._headers = headers

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, body: str) -> None:
        self._body = body

    @property
    def duplicati_url(self) -> str:
        return self._duplicati_url

    @duplicati_url.setter
    def duplicati_url(self, duplicati_url:str) -> None:
        self._duplicati_url = duplicati_url

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, tag:str) -> None:
        self._tag = tag

    def as_dict(self) -> dict:
        return {
            "body": self._body + ("\n"+self._duplicati_url) if self._duplicati_url else "",
            "tag": self._tag
        }
