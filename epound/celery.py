# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# from django.conf import settings
# from celery.decorators import task

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'epound.settings')
# app = Celery('epound')

# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(settings.INSTALLED_APPS)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

# @task(name="sum_two_numbers")
# def add(x, y):
#     return x + y
