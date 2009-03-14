
import os

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "oebfare.settings"

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()