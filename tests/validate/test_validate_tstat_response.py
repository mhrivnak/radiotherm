import json

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from radiotherm.validate import validate_tstat_response, RadiothermTstatError
from tests.validate.test_validate_response import TestValidateResponse


class TestValidateTStatResponse(TestValidateResponse):
    VALIDATE_RESPONSE = staticmethod(validate_tstat_response)
    SIMPLE_RETURN_VALUE = {"tmode": 1, "fmode": 2, "temp": 78, "hold": 1}
    COMPLEX_RETURN_VALUE = SIMPLE_RETURN_VALUE
    TRANSIENT_ERROR_RETURN_VALUE = {
        "tmode": -1,
        "fmode": 2,
        "temp": -1,
        "hold": 1
    }

    def test_json_transient_error(self):
        response = self.build_mock_response(200,
                                            self.TRANSIENT_ERROR_RETURN_VALUE)
        self.assertRaises(RadiothermTstatError, self.VALIDATE_RESPONSE,
                          response)

    def test_content_transient_error(self):
        response = self.build_mock_response(200)
        self.assertRaises(RadiothermTstatError, self.VALIDATE_RESPONSE,
                          response,
                          self.TRANSIENT_ERROR_RETURN_VALUE)
