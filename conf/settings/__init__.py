from split_settings.tools import include

include(
    './django.py',
    './database.py',
    './celery.py',
    './logging.py',
    './swagger.py',
    './rest_framework.py'
)