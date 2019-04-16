from epound.settings import *
import dj_database_url
import os

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['epound-prog.herokuapp.com','epoundtogo.com','www.epoundtogo.com']

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

AWS_ACCESS_KEY_ID = 'AKIAZCEUNS6HSFVNYVME'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'epound-prog'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

DEFAULT_FILE_STORAGE = 'epound.storage_backends.MediaStorage'

MEDIA_URL = ''

DATABASES['default'] = dj_database_url.config()

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES['default'] = dj_database_url.config()

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


