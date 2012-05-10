from mock import MagicMock

from tests.base_test_case import BaseTestCase
from radiotherm.fields import Field

class TestBuildGetReturn(BaseTestCase):
    INT_RETURN_VALUE = {'fake' : 1}
    NO_NAME_RETURN_VALUE = 72

    def test_with_name(self):
        field = Field('/fake', 'fake')
        ret = field._build_get_return(self.INT_RETURN_VALUE)
        self.assertTrue('raw' in ret)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret['raw'], self.INT_RETURN_VALUE['fake'])

    def test_without_name(self):
        field = Field('/fake', None)
        ret = field._build_get_return(self.NO_NAME_RETURN_VALUE)
        self.assertTrue('raw' in ret)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret['raw'], self.NO_NAME_RETURN_VALUE)

    def test_with_human(self):
        field = Field('/fake', 'fake', {0: 'Off', 1: 'On'})
        field._convert_to_human = MagicMock(return_value='On')
        ret = field._build_get_return(self.INT_RETURN_VALUE)
        self.assertTrue('raw' in ret)
        self.assertTrue('human' in ret)
        self.assertEqual(ret['human'], 'On')
