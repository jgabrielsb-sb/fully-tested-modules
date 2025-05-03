import os
from pathlib import Path

from .config import LOG_DIR

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  # keep third-party loggers
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'modules_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'modules.log'),
            'maxBytes': 5_000_000,
            'backupCount': 5,
            'level': 'DEBUG',
        },
        'string_operations_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'string_operations.log'),
            'maxBytes': 5_000_000,
            'backupCount': 5,
        },
        'file_service_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'file_service.log'),
            'maxBytes': 5_000_000,
            'backupCount': 5,
        },
        'email_service_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'email_service.log'),
            'maxBytes': 5_000_000,
            'backupCount': 5,
        }
    },
    'loggers': {
        'modules': {
            'handlers': ['console', 'modules_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'string_operations': {
            'handlers': ['console', 'modules_file', 'string_operations_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'file_service': {
            'handlers': ['console', 'modules_file', 'file_service_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'email_service': {
            'handlers': ['console', 'modules_file', 'email_service_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}