web: gunicorn  epound.wsgi --log-file - --log-level debug
worker: celery -A epound worker -events -loglevel info
beat: celery -A epound beat