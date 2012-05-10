import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

class BaseTestCase(unittest.TestCase):
    @staticmethod
    def _get_urlopen_import_path():
        if sys.version_info < (3,0):
            return 'urllib2.urlopen'
        else:
            return 'urllib.request.urlopen'
