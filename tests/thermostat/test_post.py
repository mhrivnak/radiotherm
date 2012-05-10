from mock import patch, MagicMock

from tests.base_test_case import BaseTestCase
from radiotherm.thermostat import Thermostat

URL = 'http://192.168.0.2/fake'
IP = '192.168.0.2'
POST_VALUE = 'stuff'
FAKE_REQUEST = 'this is a fake request'

class TestPost(BaseTestCase):
    @patch('radiotherm.thermostat.Thermostat._construct_url',
            MagicMock(return_value=URL))
    @patch(BaseTestCase._get_urlopen_import_path().replace('urlopen', 'Request'),
            MagicMock(return_value=FAKE_REQUEST))
    def test_calls_urlopen(self):
        with patch(self._get_urlopen_import_path()) as mock_urlopen:
            tstat = Thermostat(IP)
            tstat.post('/fake', POST_VALUE)
            mock_urlopen.assert_called_once_with(FAKE_REQUEST)

    @patch('radiotherm.thermostat.Thermostat._construct_url',
            MagicMock(return_value=URL))
    @patch(BaseTestCase._get_urlopen_import_path(),
            MagicMock(return_value=FAKE_REQUEST))
    def test_creates_request(self):
        with patch(self._get_urlopen_import_path().replace('urlopen', 'Request')) as mock_request:
            tstat = Thermostat(IP)
            tstat.post('/fake', POST_VALUE)
            mock_request.assert_called_once_with(URL, POST_VALUE, Thermostat.JSON_HEADER)
