release: python manage.py migrate
web: gunicorn rideshare.wsgi
celery: celery -A rideshare.celery worker --pool=solo -l info
celerybeat: celery -A rideshare beat -l info
celeryworker: celery -A rideshare.celery worker & celery -A rideshare beat --pool=solo -l INFO & wait -n