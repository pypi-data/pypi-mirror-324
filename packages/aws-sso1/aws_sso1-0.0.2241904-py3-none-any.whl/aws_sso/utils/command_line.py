from typing import Dict, List, NamedTuple, Type, Union
from argparse import Namespace


def namespace_to_tuple(args: Namespace, tuple_type: Type[NamedTuple]) -> NamedTuple:
    fields = tuple_type._fields
    data = {field: getattr(args, field, None) for field in fields}
    return tuple_type(**data)


def extend_parsers(parsers, names: Union[List[str], str], service: bool = True, target: str = 'action'):
    common_params = dict(parsers=parsers, service=service, target=target)
    if isinstance(names, List):
        return _extend_parsers_multi(names=names, **common_params)
    else:
        return _extend_parsers_single(name=names, **common_params)


def _extend_parsers_single(parsers, name: str, service: bool, target: str):
    parser = parsers.add_parser(name)
    if service:
        parser.add_argument('--service', type=str, required=True)
    parser.add_argument(f'--{target}', type=str, required=True)
    return parser


def _extend_parsers_multi(parsers, names: List[str], service: bool, target: str) -> Dict:
    return {name: _extend_parsers_single(parsers, name, service, target) for name in names}
