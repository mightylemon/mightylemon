#!/usr/bin/env python

import os
import sys

sys.path.insert(0, "/home/brian/www/python/django")
sys.path.insert(0, "/home/brian/www/python")
sys.path.insert(0, "/home/brian/www/python/oebfare")

os.environ["DJANGO_SETTINGS_MODULE"] = "oebfare.settings"

from django.core.servers.fastcgi import runfastcgi

def main():
    runfastcgi(**{
        "method": "threaded",
        "daemonize": "true",
        "host": "127.0.0.1",
        "port": "4900",
        "pidfile": "/home/brian/oebfare.pid",
    })

if __name__ == "__main__":
    main()
