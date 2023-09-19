import os
import django
from django.template.base import Template
from django.conf import settings
from django.template.engine import Engine 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


h = '<h1>Hello world</h1>'

Template(h)