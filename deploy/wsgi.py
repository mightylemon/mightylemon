#!/usr/bin/env python

import sys
import os

current_dir = os.path.dirname(__file__)

def setup_environ(settings):
    """
    Put the directory above and its parent on to the sys.path to ensure
    simpler setup.
    """
    sys.path.insert(0, os.path.realpath(os.path.join(current_dir, "../")))
    sys.path.insert(0, os.path.realpath(os.path.join(current_dir, "../../")))
    os.environ["DJANGO_SETTINGS_MODULE"] = settings

setup_environ("oebfare.settings")

from cherrypy.wsgiserver import CherryPyWSGIServer
from django.core.handlers.wsgi import WSGIHandler

def write_pid():
    fp = open(os.path.join(current_dir, "oebfare.pid"), "wb")
    fp.write(str(os.getpid()))
    fp.close()

def daemonize():
    """
    Detach from the terminal and continue as a daemon
    """
    # swiped from twisted/scripts/twistd.py
    # See http://www.erlenstar.demon.co.uk/unix/faq_toc.html#TOC16
    if os.fork():   # launch child and...
        os._exit(0) # kill off parent
    os.setsid()
    if os.fork():   # launch child and...
        os._exit(0) # kill off parent again.
    os.umask(077)
    null = os.open('/dev/null', os.O_RDWR)
    for i in range(3):
        try:
            os.dup2(null, i)
        except OSError, e:
            if e.errno != errno.EBADF:
                raise
    os.close(null)

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
    daemonize()
    write_pid()
    try:
        httpd.start()
    except KeyboardInterrupt:
        httpd.stop()

if __name__ == "__main__":
    main()
