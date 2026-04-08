import logging
import sys
import json
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs as structured JSON.
    This is the industry standard for production logs (easy to parse in Datadog/Splunk/ELK).
    """
    def format(self, record):
        # Base log data
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Include any exception tracebacks if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        # Add any extra data passed via the `extra={...}` dictionary in the logger call
        # We filter out standard logging attributes to only keep our custom ones
        standard_attrs = {
            "args", "asctime", "created", "exc_info", "exc_text", "filename", 
            "funcName", "levelname", "levelno", "lineno", "module", "msecs", 
            "message", "msg", "name", "pathname", "process", "processName", 
            "relativeCreated", "stack_info", "thread", "threadName"
        }
        for key, value in record.__dict__.items():
            if key not in standard_attrs:
                log_record[key] = value
                
        return json.dumps(log_record)

def setup_logger():
    """
    Sets up a logger that writes readable text to the console, 
    and structured JSON to a file named 'app.log'.
    """
    logger = logging.getLogger("country_agent")
    logger.setLevel(logging.INFO)
    
    # 1. Console Handler (Readable text for local development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    
    # 2. File Handler (Structured JSON for production)
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(JSONFormatter())
    
    # Add both handlers to our logger
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger

# Export the logger instance
logger = setup_logger()
