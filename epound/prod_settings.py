from .settings import *
import os

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'epoundtg'
SEND_GRID_API_KEY = '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'
EMAIL_HOST_PASSWORD = 'epoundscorp2018'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
