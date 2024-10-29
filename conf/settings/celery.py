from decouple import config

CELERY_BROKER = config('CELERY_BROKER')
CELERY_BACKEND = config('CELERY_BACKEND')