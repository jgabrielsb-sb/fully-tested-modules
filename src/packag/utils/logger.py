import logging
import logging.config
import os
from pathlib import Path
from packag.config.logging_config import LOGGING_CONFIG

LOG_DIR = Path(os.getenv('LOG_DIR'))
os.makedirs(LOG_DIR, exist_ok=True)
logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name):
    return logging.getLogger(name)