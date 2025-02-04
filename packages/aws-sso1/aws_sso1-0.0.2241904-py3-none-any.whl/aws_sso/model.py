from typing import NamedTuple, Optional


class CommonParams(NamedTuple):
    service: Optional[str] = None
    action: Optional[str] = None
    aws_dir: str = '~/.aws'
    config_dir: str = '~/.config'
