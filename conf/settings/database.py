from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  config('PG_NAME', default='postgres'),
        'USER': config('PG_USER', default='postgres'),
        'PASSWORD': config('PG_PASSWORD', default='postgres'),
        'HOST': config('PG_HOST', default='localhost'),
        'PORT': config('PG_PORT', default='5432'),
    }
}