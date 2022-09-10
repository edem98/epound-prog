from .settings import *
import dj_database_url

SECRET_KEY = '9gr3=4*i(v8!zcjf%1@1=#gf4=8fnl!^qd-%(hxuh^hsv6!@z%'

DEBUG = True
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['142.93.122.54','epoundtogo.com','www.epoundtogo.com','127.0.0.1', 'epound.herokuapp.com']

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True

DEFAULT_FILE_STORAGE = 'epound.storage_backends.MediaStorage'

MEDIA_URL = ''

DEBUG = True
TEMPLATE_DEBUG = True


ADMINS = [('Serge', 'edemserge.kossi@gmail.com'), ('Serge', 'edems.kossi@gmail.com'), ]

EMAIL_BACKEND = ''
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
SEND_GRID_API_KEY = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

## Database conf

DATABASES['default'] = dj_database_url.config(conn_max_age=600)
