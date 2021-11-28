release: python manage.py migrate
web: gunicorn rideshare.wsgi
celery: celery -A rideshare.celery worker --pool=solo -l info
celerybeat: celery -A rideshare beat -l info
