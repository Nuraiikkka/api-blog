from decouple import config 

from settings.base import * #noqa 


DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postqgresql_psycopg2',
        'NAME': config("BLOG_POSTQGRES_DB", cast=str),
        'USER': config("BLOG_POSTQGRES_USER", cast=str),
        'PASSWORD': config("BLOG_POSTQGRES_PASSWORD", cast=str),
        'HOST': config("BLOG_POSTQGRES_HOST", cast=str),
        'PORT': config("BLOG_POSTQGRES_PORT", cast=str),
    }
}