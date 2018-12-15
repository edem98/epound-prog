web: gunicorn  epound.wsgi --log-file - --log-level debug
worker: celery -A epound worker -l info
beat: celery -A epound beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler