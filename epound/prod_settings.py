from .settings import *
import os

SECRET_KEY = '9gr3=4*i(v8!zcjf%1@1=#gf4=8fnl!^qd-%(hxuh^hsv6!@z%'

DEBUG = True
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['142.93.122.54','epoundtogo.com','www.epoundtogo.com']

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

AWS_ACCESS_KEY_ID = 'AKIAZCEUNS6HSFVNYVME'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'epound-prog'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "epound",
        'USER': "serge",
        'PASSWORD': "sergedem92639417",
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True

DEFAULT_FILE_STORAGE = 'epound.storage_backends.MediaStorage'

MEDIA_URL = ''

DEBUG = True
TEMPLATE_DEBUG = True


ADMINS = [('Serge', 'edemserge.kossi@gmail.com'), ('Serge', 'edems.kossi@gmail.com'), ]

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'epoundtg'
SEND_GRID_API_KEY = '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'
EMAIL_HOST_PASSWORD = 'epoundscorp2018'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


CACHES = {
    "default": {
         "BACKEND": "redis_cache.RedisCache",
         "LOCATION": os.environ.get('REDIS_URL'),
    }
}

celery_url = 'redis://h:pbbd2da2ab291ec09b122ec68ae11a84ccc97a8991f727b8a87fdaa9774eac775@ec2-54-209-190-123.compute-1.amazonaws.com:62509'

BROKER_URL = celery_url
CELERY_RESULT_BACKEND = celery_url
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/London'
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_BROKER_URL = celery_url


