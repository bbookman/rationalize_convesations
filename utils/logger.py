import os
import logbook
import traceback
from datetime import datetime
import sys

# Generate log filename with date-time
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # Ensure log directory exists

log_filename = datetime.now().strftime("rationaizer_%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join(log_dir, log_filename)

# Create handlers for both file and stderr
format_string = '[{record.time:%Y-%m-%d %H:%M:%S}] {record.level_name}: {record.channel}: {record.filename}:{record.lineno} - {record.message}'

# Create file handler with immediate flushing
class FlushingFileHandler(logbook.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.stream.flush()  # Force flush after each write
        os.fsync(self.stream.fileno())  # Force write to disk

# Initialize handlers
file_handler = FlushingFileHandler(
    filename=log_path,
    mode='a',  # Append mode
    level='DEBUG',
    format_string=format_string,
    bubble=True,
    encoding='utf-8'
)

stderr_handler = logbook.StderrHandler(
    level='DEBUG',
    format_string=format_string,
    bubble=True
)

# Set up logging context
def setup_logging():
    # Push handlers in the correct order
    stderr_handler.push_application()
    file_handler.push_application()
    
    # Test the logging setup
    log = logbook.Logger('Rationalizer')
    log.debug("Logging system initialized")
    return log

# Initialize logging
log = setup_logging()

# Verify log file is writable
with open(log_path, 'a') as f:
    f.write("=== Logger Initialization Complete ===\n")
    f.flush()
    os.fsync(f.fileno())
