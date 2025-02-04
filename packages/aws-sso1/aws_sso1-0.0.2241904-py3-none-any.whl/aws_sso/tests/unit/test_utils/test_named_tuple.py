from ....utils import combine_named_tuples, pick_class_name
from nose.tools import assert_equal, assert_in
from parameterized import parameterized
from typing import Any, List, NamedTuple
from unittest import TestCase


class A(NamedTuple):
    message: str = 'hello world'


class B(NamedTuple):
    count: int = 1


class PickClassNameTest(TestCase):

    @parameterized.expand([
        (['A', 'B'], True, False, 'A'),
        (['A', 'B'], False, True, 'B'),
    ])
    def test_pick_class_name(self, items: List[str], pick_first: bool, pick_last: bool, expected: str):
        result = pick_class_name(items, pick_first=pick_first, pick_last=pick_last)
        assert_equal(result, expected)


class CombineNamedTuplesTest(TestCase):

    def test_combine_named_tuples(self):
        a = A(message='hello')
        b = B(count=5)
        combined = combine_named_tuples(a, b, class_name='Combined')
        assert_equal(combined.message, 'hello')
        assert_equal(combined.count, 5)
        assert_equal(combined.__class__.__name__, 'Combined')
