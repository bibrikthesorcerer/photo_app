from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  config('POSTGRESQL_NAME'),
        'USER': config('POSTGRESQL_USER'),
        'PASSWORD': config('POSTGRESQL_PASSWORD'),
        'HOST': config('POSTGRESQL_HOST'),
        'PORT': config('POSTGRESQL_PORT'),
    }
}