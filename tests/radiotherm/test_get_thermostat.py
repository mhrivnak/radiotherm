from mock import patch, MagicMock

import radiotherm
from tests.base_test_case import BaseTestCase

IP = '192.168.0.2'
MODEL = 'CT50 V1.94'

class TestGetThermostat(BaseTestCase):
    @patch('radiotherm.discover.discover_address')
    @patch('radiotherm.thermostat.CommonThermostat.model')
    def test_without_address(self, mock_model, mock_discover_address):
        radiotherm.get_thermostat()
        mock_discover_address.assert_called_once_with()

    @patch('radiotherm.thermostat.CommonThermostat.model')
    def test_creates_common_tstat(self, mock_model):
        with patch('radiotherm.thermostat.CommonThermostat.__init__',
                MagicMock(return_value=None)) as mock_init:
            radiotherm.get_thermostat(IP)
            mock_init.assert_called_once_with(IP)

    @patch('radiotherm.get_thermostat_class')
    def test_model_found(self, mock_get_class):
        mock_model = MagicMock()
        mock_model.get = lambda x: MODEL
        with patch('radiotherm.thermostat.CommonThermostat.model',
                mock_model):
            ret = radiotherm.get_thermostat(IP)
            mock_get_class.assert_called_once_with(MODEL)

    @patch('radiotherm.thermostat.CommonThermostat.model', MagicMock(return_value=None))
    def test_model_not_found(self):
        ret = radiotherm.get_thermostat(IP)
        self.assertIsNone(ret)
