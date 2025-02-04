from ....model import CommonParams
from ....services import HelloParams, HelloWorker
from ....utils import mock_input_output
from nose.tools import assert_equal
from parameterized import parameterized
from unittest import TestCase
import os


class HelloTest(TestCase):

    @staticmethod
    def build_hello(message: str, count: int) -> str:
        return os.linesep.join([message] * count)

    @parameterized.expand([
        ('this is the kitchen', 4),
        ('hello world', 1)
    ])
    def test_hello(self, message: str, count: int):
        expected_output = self.build_hello(message, count)
        params = HelloParams(message=message, count=count)
        common_params = CommonParams(service='print', action='print')
        worker = HelloWorker(common_params, params)

        with mock_input_output() as mock_io:
            worker()
            mock_io.stdout.seek(0)
            output = mock_io.stdout.read().strip()

        assert_equal(output, expected_output)

    def test_read(self):
        assert_equal('hello world', HelloWorker.read())
