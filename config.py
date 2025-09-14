import os
import sys
from logger import Logging

class Config:
    def __init__(self):
        self._LOG_LEVEL:str = os.getenv("LOG_LEVEL", "").upper() if os.getenv("LOG_LEVEL", "").upper() in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] else "ERROR"

        # Create logger in here so we can error and exit if .env is misconfigured
        logger = Logging(self._LOG_LEVEL)

        self._NOTIFICATION_SERVICE:str = os.getenv("NOTIFICATION_SERVICE", "").lower()
        self._WEBHOOK_URL:str = os.getenv("WEBHOOK_URL", "")

        if (not self._NOTIFICATION_SERVICE or not self._WEBHOOK_URL):
            logger.get_instance().error("Error in .env file. required key NOTIFICATION_SERVICE or WEBHOOK_URL is empty")
            sys.exit(1)
        elif (self._NOTIFICATION_SERVICE not in ["apprise", "discord"]):
            logger.get_instance().error("Error in .env file. NOTIFICATION_SERVICE key is not apprise nor discord")
            sys.exit(1)

        self._DUPLICATI_URL:str = os.getenv("DUPLICATI_URL", "")
        self._APPRISE_TAG:str = os.getenv("APPRISE_TAG", "") if os.getenv("APPRISE_TAG", "") else "all"
        self._PORT:int = int(os.getenv("PORT", "")) if os.getenv("PORT", "").isdecimal() else 8123

    
    @property
    def LOG_LEVEL(self):
        return self._LOG_LEVEL
    
    @property
    def NOTIFICATION_SERVICE(self):
        return self._NOTIFICATION_SERVICE
    
    @property
    def WEBHOOK_URL(self):
        return self._WEBHOOK_URL

    @property
    def DUPLICATI_URL(self):
        return self._DUPLICATI_URL
    
    @property
    def APPRISE_TAG(self):
        return self._APPRISE_TAG

    @property
    def PORT(self):
        return self._PORT