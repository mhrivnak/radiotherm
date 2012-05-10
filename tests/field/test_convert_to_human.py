from radiotherm.fields import Field
from tests.base_test_case import BaseTestCase

class TestConvertToHuman(BaseTestCase):
    def setUp(self):
        self.field = Field('/fake', 'fake', {
            0 : 'Off',
            1 : 'On',
            'foo' : 'Foo'
        })

    def test_convert_int_success(self):
        ret = self.field._convert_to_human(0)
        self.assertEqual(ret, 'Off')

    def test_convert_int_fail(self):
        self.assertRaises(AttributeError, self.field._convert_to_human, 3)

    def test_convert_string_success(self):
        ret = self.field._convert_to_human('foo')
        self.assertEqual(ret, 'Foo')

    def test_convert_string_fail(self):
        self.assertRaises(AttributeError, self.field._convert_to_human, 'bar')
