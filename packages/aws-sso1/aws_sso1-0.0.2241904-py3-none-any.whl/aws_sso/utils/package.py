from contextlib import contextmanager, ExitStack
from typing import ContextManager, Iterator, List, TypeVar, Union

T = TypeVar('T')
ItemOrList = Union[T, List[T]]


def get_package_root() -> str:
    return __package__.split('.')[0]


def iter_list_items(*args: ItemOrList[T]) -> Iterator[T]:
    for item_or_list in args:
        if isinstance(item_or_list, list):
            yield from item_or_list
        else:
            yield item_or_list


@contextmanager
def combine_contexts(*contexts: ContextManager[T]) -> Iterator[List[T]]:
    with ExitStack() as stack:
        yield [stack.enter_context(ctx) for ctx in contexts]
