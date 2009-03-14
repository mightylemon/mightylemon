
import os
from os.path import abspath, dirname, join

sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "oebfare.settings"

sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()