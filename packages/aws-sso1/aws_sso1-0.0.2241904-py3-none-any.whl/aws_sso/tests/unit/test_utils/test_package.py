from ....utils import combine_contexts, get_package_root, iter_list_items
from contextlib import contextmanager
from nose.tools import assert_equal
from parameterized import parameterized
from typing import ContextManager, List
from unittest import TestCase


class PackageTest(TestCase):

    def test_package_root(self):
        assert_equal(get_package_root(), 'aws_sso')

    @classmethod
    def build_example_context_manager(cls, queue: list, stack: list) -> ContextManager:
        @contextmanager
        def example(n: int):
            queue.append(n)
            try:
                yield
            finally:
                stack.append(n)
        return example

    def test_combine_contexts(self):
        queue, stack = [], []
        contexts = [self.build_example_context_manager(queue, stack)(i) for i in range(3)]
        with combine_contexts(*contexts):
            assert_equal(queue, [0, 1, 2])
        assert_equal(stack, [2, 1, 0])

    @parameterized.expand([
        ([1, [2, 3], 4], [1, 2, 3, 4]),
        (['a', ['b', 'c'], 'd'], ['a', 'b', 'c', 'd']),
    ])
    def test_iter_list_items(self, input_list: List, expected: List):
        result = list(iter_list_items(*input_list))
        assert_equal(result, expected)
