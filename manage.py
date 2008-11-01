#!/usr/bin/env python

import sys
from os.path import abspath, dirname, join

sys.path.insert(0, abspath(join(dirname(__file__), "externals")))

from django.core.management import execute_manager

try:
    import settings # test comment
except ImportError, e:
    sys.stderr.write("cannot find settings: %s\n" % e)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
