from decouple import config
LOG_REQUESTS = True
LOG_USER_ATTRIBUTE = "username"
NO_REQUEST_ID = "no ID"
LOGGING_ENABLED = config('LOGGING_ENABLED', default=True, cast=bool)
if LOGGING_ENABLED:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'request_id': {
                '()': 'log_request_id.filters.RequestIDFilter'
            },
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        'formatters': {
            'standart': {
                'format': '{levelname:8} [{asctime}] [{request_id}] {name}: {message}',
                'style': '{'
            },
            'rich': {
                'format': '[{asctime}] [bold white on cyan]\\[{request_id}][/] [bold magenta]{name}[/]: {message}',
                'style': '{'
            },
        },
        'handlers': {
            'console': {
                'level': config('LOG_LEVEL', 'INFO'),
                'filters': ['request_id'],
                'formatter': 'rich',
                # rich handler settings
                'class': 'rich.logging.RichHandler',
                'show_time': False,
                'rich_tracebacks': True,
                'markup': True
            },
            'file': {
                'level': config('LOG_LEVEL', 'INFO'),
                'filters': ['request_id'],
                'formatter': 'standart',
                'class': 'logging.FileHandler',
                'filename': config('LOG_FILE_PATH'),
            }
        },
        'loggers': {
            'daphne': {
                'handlers': ['console', 'file'],
                'level': config('DAPHNE_LOG_LEVEL', config('LOG_LEVEL', 'INFO')),
                'propagate': False
            },
            'django.channels': {
                'handlers': ['console', 'file'],
                'level': config('CHANNELS_LOG_LEVEL', config('LOG_LEVEL', 'ERROR')),
                'propagate': False
            },
            'django': {
                'handlers': ['console', 'file'],
                'level': config('DJANGO_LOG_LEVEL', config('LOG_LEVEL', 'INFO')),
                'propagate': True
            },
            'django.db.backends': {
                'handlers': ['console', 'file'],
                'filters': ['require_debug_true'],
                'level': config('DB_LOG_LEVEL', config('LOG_LEVEL', 'DEBUG')),
                'propagate': False
            },
        },
    }
