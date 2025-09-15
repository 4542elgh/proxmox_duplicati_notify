import os
import logging

class Logging:
    """
    Wrapper for builtin logging module.

    This module create a global logger with both console and file handlers. 
    Log messages are written to stdout and a `log.txt` file in the current working directory

    You can use logging.getLogger() to gain access to global logger.
    All other methods are identical to builtin logging (with help from argument forwarding)
    """
    def __init__(self, log_level:str, mode:str="w") -> None:
        # Dont need to keep track of instance since its global
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Stdout and log.txt
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        file_handler = logging.FileHandler(os.path.join(os.getcwd(), "log.txt"), mode=mode, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, *args, **kwargs) -> None:
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        self.logger.error(*args, **kwargs)
