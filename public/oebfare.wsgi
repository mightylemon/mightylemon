#!/usr/bin/env python

import os
import sys

sys.path.insert(0, "../")
sys.path.insert(1, "../../")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

from cherrypy.wsgiserver import CherryPyWSGIServer
from django.core.handlers.wsgi import WSGIHandler

def main():
    params = sys.argv[1:]
    if params:
        host, port = params
        if host == "0":
            host = "0.0.0.0"
        port = int(port)
    else:
        host, port = "127.0.0.1", 8000
    httpd = CherryPyWSGIServer((host, port), WSGIHandler(),
        server_name="localhost")
    try:
        httpd.start()
    except KeyboardInterrupt:
        httpd.stop()

if __name__ == "__main__":
    main()
