import json

try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch, MagicMock

from radiotherm.thermostat import CommonThermostat
from tests.base_test_case import BaseTestCase

COMMAND = '/sys/command'
IP = '192.168.0.2'
JSON_VALUE = json.dumps({'command' : 'reboot'}).encode('utf-8')
RESPONSE_VALUE = 'this is a response value'

class TestReboot(BaseTestCase):
    @patch('radiotherm.thermostat.Thermostat.post')
    @patch('radiotherm.validate.validate_response')
    def test_calls_post(self, mock_validate_response, mock_post):
        tstat = CommonThermostat(IP)
        tstat.reboot()
        mock_post.assert_called_once_with(COMMAND, JSON_VALUE)

    @patch('radiotherm.thermostat.Thermostat.post', MagicMock(return_value=RESPONSE_VALUE))
    @patch('radiotherm.validate.validate_response')
    def test_calls_validate_response(self, mock_validate_response):
        tstat = CommonThermostat(IP)
        tstat.reboot()
        mock_validate_response.assert_called_once_with(RESPONSE_VALUE)
