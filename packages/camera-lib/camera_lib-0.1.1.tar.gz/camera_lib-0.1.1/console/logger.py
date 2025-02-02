import logging
from PyQt5.QtCore import pyqtSignal, QObject

from console.loghandler import LogHandler

class Logger():
    """Singleton Logger that emits log messages via PyQt signals."""
    
    _instance = None  # Singleton instance

    def __new__(cls):
        """Ensure only one instance of the logger exists."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        """Set up the logger."""
        super().__init__()  # Initialize QObject
        self.logger = logging.getLogger("Logger")
        self.logger.setLevel(logging.DEBUG)  # Log Level

        # Avoid duplicate handlers
        if not self.logger.hasHandlers():
            self.handler = LogHandler()
            self.handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(self.handler)

    def get_logger(self):
        """Return the logger instance."""
        return self.logger
    
