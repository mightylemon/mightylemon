import glob
import logging
import os
import re
import sys
import zipfile
import os.path


ZIP_SKIP_RE = re.compile('\.svn|\.pyc|\.[pm]o')
IGNORED_CONTRIB = ('admin', 'gis', 'comments', 'localflavor', 'databrowse')
ROOT_DIR = os.path.dirname(__file__)

def bootstrap(only_check_for_zips=False):
  logging.info('Beginning bootstrap...')
  l = os.listdir('vendor')
  for vendor_lib in l:
    if vendor_lib.startswith('.'):
      continue
    if only_check_for_zips and os.path.exists('%s.zip' % vendor_lib):
      continue
    logging.info('Building zip for %s...' % vendor_lib)
    zip_vendor_lib(vendor_lib)
  logging.info('Finishing bootstrap.')

def monkey_patch_skipped_files():
  logging.info('Monkey patching dev_appserver...')
  from google.appengine.tools import dev_appserver as da

  def _patch(logical_filename, normcase=os.path.normcase):
    """Determines if a file's path is accessible.

    This is an internal part of the IsFileAccessible implementation.

    Args:
      logical_filename: Absolute path of the file to check.
      normcase: Used for dependency injection.

    Returns:
      True if the file is accessible, False otherwise.
    """
    if da.IsPathInSubdirectories(logical_filename, [da.FakeFile._root_path],
                              normcase=normcase):
      relative_filename = logical_filename[len(da.FakeFile._root_path):]

      #if da.FakeFile._skip_files.match(relative_filename):
      #  logging.warning('Blocking access to skipped file "%s"',
      #                  logical_filename)
      #  return False

      if da.FakeFile._static_file_config_matcher.IsStaticFile(relative_filename):
        logging.warning('Blocking access to static file "%s"',
                        logical_filename)
        return False

    if logical_filename in da.FakeFile.ALLOWED_FILES:
      return True

    if da.IsPathInSubdirectories(logical_filename,
                              da.FakeFile.ALLOWED_SITE_PACKAGE_DIRS,
                              normcase=normcase):
      return True

    allowed_dirs = da.FakeFile._application_paths | da.FakeFile.ALLOWED_DIRS
    if (da.IsPathInSubdirectories(logical_filename,
                               allowed_dirs,
                               normcase=normcase) and
        not da.IsPathInSubdirectories(logical_filename,
                                   da.FakeFile.NOT_ALLOWED_DIRS,
                                   normcase=normcase)):
      return True

    return False
  
  da.FakeFile._IsFileAccessibleNoCache = staticmethod(_patch)

def _strip_contrib(dirnames):
  for d in IGNORED_CONTRIB:
    try:
      dirnames.remove(d)
    except ValueError:
      pass

def zip_vendor_lib(lib):
  f = zipfile.ZipFile('%s.zip' % lib, 'w')

  for dirpath, dirnames, filenames in os.walk('vendor/%s' % lib):
    if dirpath == os.path.join('vendor', lib, 'contrib'):
      _strip_contrib(dirnames)

    for filename in filenames:
      name = os.path.join(dirpath, filename)
      if ZIP_SKIP_RE.search(name):
        logging.debug('Skipped (skip_re): %s', name)
        continue
      if not os.path.isfile(name):
        logging.debug('Skipped (isfile): %s', name)
        continue
      logging.debug('Adding %s...', name)
      f.write(name, name[len('vendor/'):], zipfile.ZIP_DEFLATED)

  f.close()

