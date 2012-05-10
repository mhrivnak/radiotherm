from tests.base_test_case import BaseTestCase
import radiotherm
from radiotherm.thermostat import CT50v194

class TestGetThermostatClass(BaseTestCase):
    def test_class_exists(self):
        ret = radiotherm.get_thermostat_class('CT50 V1.94')
        self.assertEqual(ret, CT50v194)

    def test_class_does_not_exist(self):
        ret = radiotherm.get_thermostat_class('CT51 V3.17')
        self.assertIsNone(ret)
