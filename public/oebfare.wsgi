#!/usr/bin/env python

import os
import sys

sys.path.insert(0, "../")
sys.path.insert(1, "../../")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from cherrypy.wsgiserver import CherryPyWSGIServer
from django.core.handlers.wsgi import WSGIHandler

def main():
    httpd = CherryPyWSGIServer(("127.0.0.1", 8000), WSGIHandler(),
        server_name="localhost")
    try:
        httpd.start()
    except KeyboardInterrupt:
        httpd.stop()

if __name__ == "__main__":
    main()
