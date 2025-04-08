import os
import shutil
import logging
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs"):
        """Initialize logger with automatic cleanup of existing log directory."""
        self.log_dir = log_dir
        

        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"log_{timestamp}.txt")
        
        # Configure logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def log(self, message, level="info"):
        """Log messages at different severity levels."""
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "debug":
            self.logger.debug(message)

    def log_exception(self, exception):
        """Log exceptions with traceback details."""
        self.logger.exception("Exception occurred", exc_info=True)
