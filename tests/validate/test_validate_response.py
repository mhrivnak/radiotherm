import json

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from radiotherm.validate import validate_response
from tests.base_test_case import BaseTestCase

class TestValidateResponse(BaseTestCase):
    VALIDATE_RESPONSE = staticmethod(validate_response)
    SIMPLE_RETURN_VALUE = {}
    COMPLEX_RETURN_VALUE = {
        'foo' : [1, 2, 3],
        'bar' : {'a' : 1, 'b' : 2}
    }
    ERROR_RETURN_VALUE = {'error' : 'stuff'}
    ERROR_MSG_RETURN_VALUE = {'error_msg' : 'stuff'}

    @staticmethod
    def build_mock_response(http_code, content=None):
        response = MagicMock()
        response.getcode = MagicMock(return_value=http_code)
        if content is not None:
            response.read = MagicMock(return_value=json.dumps(content).encode('utf-8'))
        return response

    def test_200(self):
        response = self.build_mock_response(200)
        self.VALIDATE_RESPONSE(response, self.SIMPLE_RETURN_VALUE)

    def test_404(self):
        response = self.build_mock_response(404)
        self.assertRaises(AttributeError, self.VALIDATE_RESPONSE, response,
                          self.SIMPLE_RETURN_VALUE)

    def test_json_success(self):
        response = self.build_mock_response(200, self.COMPLEX_RETURN_VALUE)
        self.VALIDATE_RESPONSE(response)

    def test_json_error(self):
        response = self.build_mock_response(200, self.ERROR_RETURN_VALUE)
        self.assertRaises(AttributeError, self.VALIDATE_RESPONSE, response)

    def test_json_error_msg(self):
        response = self.build_mock_response(200, self.ERROR_MSG_RETURN_VALUE)
        self.assertRaises(AttributeError, self.VALIDATE_RESPONSE, response)

    def test_content_error(self):
        response = self.build_mock_response(200)
        self.assertRaises(AttributeError, self.VALIDATE_RESPONSE, response,
            self.ERROR_RETURN_VALUE)

    def test_content_error_msg(self):
        response = self.build_mock_response(200)
        self.assertRaises(AttributeError, self.VALIDATE_RESPONSE, response,
            self.ERROR_MSG_RETURN_VALUE)
