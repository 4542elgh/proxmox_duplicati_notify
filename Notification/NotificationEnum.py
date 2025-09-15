from enum import Enum

class NOTIFICATION(Enum):
    """
        Enum for NotificationServices This ensures a more robust service type checking
    """
    APPRISE = "apprise"
    DISCORD = "discord"
