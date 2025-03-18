from decouple import config
LOG_REQUESTS = True
LOG_USER_ATTRIBUTE = "username"
NO_REQUEST_ID = "no ID"
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
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'rich',
            # rich handler settings
            'class': 'rich.logging.RichHandler',
            'show_time': False,
            'rich_tracebacks': True,
            'markup': True
        },
        'file': {
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'standart',
            'class': 'logging.FileHandler',
            'filename': 'photo_app.log',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': config('LOG_LEVEL', 'INFO'),
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'filters': ['require_debug_true'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}
