import json

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

from tests.base_test_case import BaseTestCase
from radiotherm.thermostat import CommonThermostat

PROGRAM = {1:[480,73,1380,70,1380,70,1380,70]}

class TestSetDayProgram(BaseTestCase):
    @patch('radiotherm.thermostat.CommonThermostat.post')
    def test_calls_post(self, mock_post):
        tstat = CommonThermostat('192.168.0.1')
        tstat.set_day_program('cool', 'tue', PROGRAM)
        mock_post.assert_called_once_with('/tstat/program/cool/tue', json.dumps(PROGRAM).encode('utf-8'))
