import abc

class MessageService(abc.ABC):
    """
    Abstract base class for notification message services.

    Subclasses must implement body message, webhook URL assignment, 
    and json serialization (`as_dict`). This ensures consistent 
    behavior across different notification backends. 
    
    duplicati_url and headers are shared across all objects. Since they are not part of the requests json payload, they can be stored on abstract class

    Attributes:
        _webhook_url (str): The webhook endpoint for the notification service.
        _headers (dict): Optional headers used when sending HTTP requests.
    """
    # This will get inherit to all subclass
    _webhook_url:str = ""
    _headers: dict = {}

    @property
    @abc.abstractmethod
    def body(self) -> str:
        pass

    @body.setter
    @abc.abstractmethod
    def body(self, body: str) -> None:
        pass

    @property
    @abc.abstractmethod
    def duplicati_url(self) -> str:
        pass

    @duplicati_url.setter
    @abc.abstractmethod
    def duplicati_url(self, duplicati_url: str) -> None:
        pass

    @abc.abstractmethod
    def as_dict(self) -> dict:
        # Return the json representation of the final payload. This might be different depending on the messaging platform used
        pass

    # This will get inherit to all subclass
    @property
    def webhook_url(self) -> str:
        return self._webhook_url

    @webhook_url.setter
    def webhook_url(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, headers: dict) -> None:
        self._headers = headers 

