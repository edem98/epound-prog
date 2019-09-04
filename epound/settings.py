"""
Django settings for epound project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from celery.schedules import crontab
import djcelery

djcelery.setup_loader()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6fa9=4*i(v8!zcjf%1@1=#gf4=8fnl!^qd-%(hxuh^hsv6!@z%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'jet',
    'dal',
    'dal_select2',
    'polymorphic',
    'suit_ckeditor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admindocs',
    'rest_framework',
    'gunicorn',
    'djcelery',
    'django_celery_beat',
    'daterange_filter',
    'storages',
    'sorl.thumbnail',
    # 'django_extensions',
    # mes apps
    'archive.apps.ArchiveConfig',
    'compte.apps.CompteConfig',
    'dashboard.apps.DashboardConfig',
    'emision.apps.EmissionConfig',
    'membre.apps.MembreConfig',
    'octroi.apps.OctroiConfig',
    'reconversion.apps.ReconversionConfig',
    'services.apps.ServicesConfig',
    'ecommerce.apps.EcommerceConfig',
    'recette.apps.RecetteConfig',
    'faqs.apps.FaqsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

ROOT_URLCONF = 'epound.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'compte.context_processors.compte_alpha',
                'compte.context_processors.compte_grenier',
                'compte.context_processors.compte_beta',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'epound.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "epound_prog",
        'USER': "serge",
        'PASSWORD': "sergedem",
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TEST': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': "epound_prog",
            'USER': "serge",
            'PASSWORD': "sergedem",
            'HOST': '127.0.0.1',
            'PORT': '5432',
        },
    }
}

# Static files
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
HOST_SCHEME = "http://"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/London'
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_BROKER_URL = 'redis://localhost:6379'

ADMINS = [('Serge', 'edemserge.kossi@gmail.com'), ('Serge', 'edems.kossi@gmail.com'), ]

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'epoundtg'
SEND_GRID_API_KEY = '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'
EMAIL_HOST_PASSWORD = 'epoundscorp2018'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SITE_ID = 1

# Using django-imperavi
NEWSLETTER_RICHTEXT_WIDGET = "suit_ckeditor.widgets.CKEditorWidget"

# Amount of seconds to wait between each email. Here 100ms is used.
NEWSLETTER_EMAIL_DELAY = 0.1

# Amount of seconds to wait between each batch. Here one minute is used.
NEWSLETTER_BATCH_DELAY = 60

# Number of emails in one batch
NEWSLETTER_BATCH_SIZE = 100

# twilo sms credentials
TWILIO_ACCOUNT_SID = 'ACfff60f15de8fe247009c9b9986b0aa97'
TWILIO_AUTH_TOKEN = '31aaff118a5b772185dc425695c54d82'
