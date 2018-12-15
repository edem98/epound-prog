from epound.settings import *
import dj_database_url
import os

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['epound-prog.herokuapp.com']

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

AWS_ACCESS_KEY_ID = 'AKIAIGR4ZJQ3GGLIG6BQ'
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