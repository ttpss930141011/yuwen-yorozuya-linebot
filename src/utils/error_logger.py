# error_handling.py
import logging
# Configure logging
errlogger = logging.getLogger("error_logger")
errlogger.setLevel(logging.ERROR)

# Create handlers
file_handler = logging.FileHandler('logs/bot_errors.log')
file_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
file_formatter = logging.Formatter(
    '%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Add handlers to the errlogger
errlogger.addHandler(file_handler)
