#!/usr/bin/env python
import sys

from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "externals")))

from django.conf import settings
from django.core.management import setup_environ, execute_from_command_line

try:
    import settings as settings_mod # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("cannot find settings: %s\n" % e)
    sys.exit(1)

# setup the environment before we start accessing things in the settings.
setup_environ(settings_mod)

path = addsitedir(join(settings.PINAX_ROOT, "libs/external_libs"), set())
if path:
    sys.path = list(path) + sys.path
sys.path.insert(0, join(settings.PINAX_ROOT, "apps/external_apps"))
sys.path.insert(0, join(settings.PINAX_ROOT, "apps/local_apps"))
sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

if __name__ == "__main__":
    execute_from_command_line()
