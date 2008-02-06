#!/usr/bin/env python

#
# Make sure the environment is setup prior to running this script. This means
# django must be in PYTHONPATH and DJANGO_SETTINGS_MODULE must be set correctly.
#

from django.core.servers.fastcgi import runfastcgi

def main():
    runfastcgi(**{
        "method": "threaded",
        "daemonize": "true",
        "host": "127.0.0.1",
        "port": "4900",
        "pidfile": "/home/brian/oebfare.pid",
    )

if __name__ == "__main__":
    main()
