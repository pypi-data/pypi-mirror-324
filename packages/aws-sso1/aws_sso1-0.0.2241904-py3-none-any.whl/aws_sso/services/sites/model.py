from enum import Enum
from typing import NamedTuple


class SiteLogin(NamedTuple):
    domain: str
    username: str
    password: str


class KeyringAction(Enum):
    read = 'get_password'
    write = 'set_password'
    delete = 'delete_password'

    @property
    def method(self) -> str:
        return self.value
