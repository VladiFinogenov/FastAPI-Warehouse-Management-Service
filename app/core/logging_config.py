import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s:%(funcName)s] %(message)s'
        },
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'formatter': 'default_formatter',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
        },
    },
    # 'loggers': {
    #     'sqlalchemy.engine': {
    #         'level': 'ERROR',
    #         'handlers': ['stream_handler', 'file_handler'],
    #         'propagate': False,
    #     },
    # },
    'root': {
        'handlers': ['stream_handler', 'file_handler'],
        'level': 'DEBUG',
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('my_logger')

def setup_logging():
    logging.config.dictConfig(LOGGING)
