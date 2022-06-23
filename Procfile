release: python manage.py migrate
web: python manage.py collectstatic --no-input; gunicorn rideshare.wsgi
celery: celery -A rideshare.celery worker --pool=solo -l info
celerybeat: celery -A rideshare beat -l info
celeryworker: celery -A rideshare.celery worker & celery -A rideshare beat -l INFO & wait -n