from celery import Celery
import os

SETTINGS_ROOT_DIRECTORY = 'config'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{SETTINGS_ROOT_DIRECTORY}.settings")

app = Celery('config')
app.config_from_object("django.conf:settings",namespace='CELERY')

# This line makes celery to look for a 'task.py' file in each django app
# Alternative: add a CELERY_IMPORTS to configurations in settings.py manually
app.autodiscover_tasks()
