from tests.base_test_case import BaseTestCase
from radiotherm.thermostat import Thermostat

class TestConstructURL(BaseTestCase):
    def test_with_ip(self):
        tstat = Thermostat('192.168.0.2')
        url = tstat._construct_url('/fake')
        self.assertEqual(url, 'http://192.168.0.2/fake')

    def test_with_fqdn(self):
        tstat = Thermostat('tstat.home.mydomain.org')
        url = tstat._construct_url('/fake')
        self.assertEqual(url, 'http://tstat.home.mydomain.org/fake')

    def test_without_leading_slash(self):
        tstat = Thermostat('192.168.0.2')
        url = tstat._construct_url('fake')
        self.assertEqual(url, 'http://192.168.0.2/fake')

    def test_trailing_slash_preserved(self):
        tstat = Thermostat('192.168.0.2')
        url = tstat._construct_url('/fake/')
        self.assertEqual(url, 'http://192.168.0.2/fake/')
