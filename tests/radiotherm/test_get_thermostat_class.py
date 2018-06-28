from tests.base_test_case import BaseTestCase
import radiotherm
from radiotherm.thermostat import CT50v194, CT80RevB, CT80


class TestGetThermostatClass(BaseTestCase):
    def test_class_exists(self):
        ret = radiotherm.get_thermostat_class('CT50 V1.94')
        self.assertEqual(ret, CT50v194)

    def test_class_base_rev_exists(self):
        ret = radiotherm.get_thermostat_class('CT80 RevB V5.94')
        self.assertEqual(ret, CT80RevB)

    def test_class_base_model_exists(self):
        ret = radiotherm.get_thermostat_class('CT80 RevA V2.94')
        self.assertEqual(ret, CT80)

    def test_class_does_not_exist(self):
        ret = radiotherm.get_thermostat_class('CT51 V3.17')
        self.assertIsNone(ret)
