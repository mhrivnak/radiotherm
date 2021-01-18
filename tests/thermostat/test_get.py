try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch, MagicMock

from tests.base_test_case import BaseTestCase
from radiotherm.thermostat import Thermostat

URL = 'http://192.168.0.2/fake'
IP = '192.168.0.2'

class TestGet(BaseTestCase):
    @patch('radiotherm.thermostat.Thermostat._construct_url',
            MagicMock(return_value=URL))
    def test_opens_url(self):
        with patch(self._get_urlopen_import_path()) as mock_urlopen:
            tstat = Thermostat(IP)
            tstat.get('/fake')
            mock_urlopen.assert_called_once_with(URL, timeout=4)
