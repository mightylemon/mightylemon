#!/usr/bin/env python
import logging
import os
import sys

from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "externals")))

# TODO(termie): hackhackhack
import settings
if settings.APP_ENGINE:
    from appengine_django import InstallAppengineHelperForDjango
    InstallAppengineHelperForDjango()
    
    for x in os.listdir('.'):
      if x.endswith('.zip'):
        if x in sys.path:
          continue
        logging.debug("Adding %s to the sys.path", x)
        sys.path.insert(1, x)

from django.conf import settings
from django.core.management import setup_environ, execute_from_command_line

try:
    import settings as settings_mod # Assumed to be in the same directory.
except ImportError, e:
    sys.stderr.write("cannot find settings: %s\n" % e)
    sys.exit(1)

# setup the environment before we start accessing things in the settings.
setup_environ(settings_mod)

sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

if __name__ == "__main__":
    execute_from_command_line()
