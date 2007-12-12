#!/usr/bin/env python
from django.core.management import execute_manager
try:
    import settings # assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("canot find settings.")
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
