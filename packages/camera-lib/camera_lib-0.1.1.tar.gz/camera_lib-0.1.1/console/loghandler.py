import logging
from PyQt5.QtCore import pyqtSignal, QObject

class LogHandler(QObject, logging.Handler):
    log_signal = pyqtSignal(str)  # Define a signal that sends log messages

    def __init__(self):
        super().__init__()
        logging.Handler.__init__(self)

    def emit(self, record):
        """Emit a log record."""
        log_entry = self.format(record)  # Format the log message
        self.log_signal.emit(log_entry)  # Emit the signal with the log message