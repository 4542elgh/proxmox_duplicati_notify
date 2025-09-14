import os
import logging

class Logging:
    def __init__(self, log_level:str) -> None:
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
        file_handler = logging.FileHandler(os.path.join(os.getcwd(), "log.txt"), mode='w', encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_instance(self) -> logging.Logger:
        return self.logger