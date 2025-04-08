import os
import logging
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs"):
        # Create a valid log file path
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)  # Ensure directory exists
        
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
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "debug":
            self.logger.debug(message)

    # Add this method to your Logger class    
    def log_exception(self, exception):
        # self.logger.error(f"Exception occurred: {str(exception)}")
        # Or use a more detailed format if needed
        self.logger.exception("Exception occurred", exc_info=True)
        # This will log the traceback along with the message
 