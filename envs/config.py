import os
import sys
from dotenv import load_dotenv
from Logging.logger import Logging

class Config:
    """
    Configuration management for environment variables and logging setup.

    This module defines a `Config` class that reads `.env` variables, exposes them through read-only properties.
    It ensures that misconfigured `.env` files cause the application to log an error and exit immediately.

    Environment Variables:
        LOG_LEVEL (str, optional): Logging level. One of ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"].
                                Defaults to "ERROR" if unset or invalid.
        NOTIFICATION_SERVICE (str, required): Notification service type ("apprise" or "discord").
        WEBHOOK_URL (str, required): Webhook URL for the configured notification service.
        DUPLICATI_URL (str, optional): URL of the Duplicati backup service. Defaults to empty string.
        APPRISE_TAG (str, optional): Tag used for Apprise notifications. Defaults to "all" if unset.
        PORT (int, optional): Port number for the service. Defaults to 8123 if unset or invalid.
    """
    def __init__(self):
        load_dotenv()
        self._LOG_LEVEL:str = os.getenv("LOG_LEVEL", "").upper() if os.getenv("LOG_LEVEL", "").upper() in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] else "ERROR"

        # Create logger in here so we can error and exit if .env is misconfigured
        logger = Logging(self._LOG_LEVEL)

        self._NOTIFICATION_SERVICE:str = os.getenv("NOTIFICATION_SERVICE", "").lower()
        self._WEBHOOK_URL:str = os.getenv("WEBHOOK_URL", "")

        if (not self._NOTIFICATION_SERVICE or not self._WEBHOOK_URL):
            logger.error("Error in .env file. required key NOTIFICATION_SERVICE or WEBHOOK_URL is empty")
            sys.exit(1)
        elif (self._NOTIFICATION_SERVICE not in ["apprise", "discord"]):
            logger.error("Error in .env file. NOTIFICATION_SERVICE key is not apprise nor discord")
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