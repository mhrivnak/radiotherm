try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from tests.base_test_case import BaseTestCase
from radiotherm.fields import ReadOnlyField

class TestReadOnlyField(BaseTestCase):
    def test_set(self):
        field = ReadOnlyField('/fake', 'fake')
        self.assertRaises(TypeError, field.__set__, MagicMock, MagicMock)
