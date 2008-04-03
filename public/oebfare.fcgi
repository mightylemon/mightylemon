#!/usr/bin/env python

import os
import sys
import linecache

sys.path.insert(0, "/home/brian/www/python/django")
sys.path.insert(0, "/home/brian/www/python")
sys.path.insert(0, "/home/brian/www/python/oebfare")

os.environ["DJANGO_SETTINGS_MODULE"] = "oebfare.settings"

from django.core.servers.fastcgi import runfastcgi

def tracer(frame, event, arg):
    if event == "line":
        lineno = frame.f_lineno
        try:
            filename = frame.f_globals["__file__"]
        except KeyError:
            filename = "unknown"
        if (filename.endswith(".pyc") or
            filename.endswith(".pyo")):
            filename = filename[:-1]
        try:
            name = frame.f_globals["__name__"]
        except KeyError:
            name = "unknown"
        line = linecache.getline(filename, lineno)
        print "%s:%s: %s" % (name, lineno, line.rstrip())
    return tracer

def main():
    print "running"
    runfastcgi(**{
        "method": "threaded",
        #"daemonize": "false",
        "host": "127.0.0.1",
        "port": "4900",
        "pidfile": "/home/brian/oebfare.pid",
    })

if __name__ == "__main__":
    #sys.settrace(tracer)
    main()
