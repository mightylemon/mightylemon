
import os
import signal

from optparse import OptionParser, make_option
from django.core.management.base import BaseCommand
from django.core.handlers.wsgi import WSGIHandler
from django.conf import settings

try:
    from cherrypy.wsgiserver import CherryPyWSGIServer
except ImportError:
    from wsgiserver import CherryPyWSGIServer

DEFAULT_HOST = getattr(settings, "WSGI_HOST", "127.0.0.1")
DEFAULT_PORT = getattr(settings, "WSGI_PORT", 8001)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-h", "--host", dest="host", default="127.0.0.1"),
        make_option("-p", "--port", dest="port", default=8001),
        make_option("-d", "--daemon", dest="daemonize", action="store_true"),
    )
    requires_model_validation = False
    
    def handle(self, *args, **options):
        self.server = CherryPyWSGIServer((options["host"], options["port"]), WSGIHandler())
        self.pidfile = os.path.join(settings.PROJECT_ROOT, "logs/wsgi.pid")
        try:
            action = args[0]
        except IndexError:
            print "You must provide an action. Possible actions are start, stop and restart."
            raise SystemExit
        if options["daemonize"]:
            daemonize()
        if action == "start":
            self.start()
        elif action == "stop":
            pid = open(self.pidfile, "r").read()
            self.stop(pid)
        elif action == "restart":
            pid = open(self.pidfile, "r").read()
            self.restart(pid)
    
    def start(self):
        writepid(self.pidfile)
        try:
            self.server.start()
        except KeyboardInterrupt:
            # likely not a daemon so make sure to shutdown properly.
            self.server.stop()
    
    def stop(self, pid):
        os.kill(int(pid), signal.SIGHUP)
    
    def restart(self, pid):
        self.stop(pid)
        self.start()
    
    def create_parser(self, prog_name, subcommand):
        """
        Create and return the ``OptionParser`` which will be used to
        parse the arguments to this command.
        """
        return OptionParser(prog=prog_name, usage=self.usage(subcommand),
            version = self.get_version(),
            option_list = self.option_list,
            conflict_handler = "resolve")

def writepid(pid_file):
    """
    Write the process ID to disk.
    """
    fp = open(pid_file, "w")
    fp.write(str(os.getpid()))
    fp.close()

def daemonize():
    """
    Detach from the terminal and continue as a daemon.
    """
    # swiped from twisted/scripts/twistd.py
    # See http://www.erlenstar.demon.co.uk/unix/faq_toc.html#TOC16
    if os.fork():   # launch child and...
        os._exit(0) # kill off parent
    os.setsid()
    if os.fork():   # launch child and...
        os._exit(0) # kill off parent again.
    os.umask(077)
    null = os.open("/dev/null", os.O_RDWR)
    for i in range(3):
        try:
            os.dup2(null, i)
        except OSError, e:
            if e.errno != errno.EBADF:
                raise
    os.close(null)