from ...abstract import AbstractService
from ...model import CommonParams
from ...utils import get_package_root, read_config, register_action, write_config
from ..sites import *
from .core import make_saml, iter_roles, assume_role
from .model import RoleTuple, Profile

from pathlib import Path
from typing import Iterator
import datetime as dt


class LoginWorker(AbstractService):

    def initialize(self):
        self.tools['sites'] = self.build_site_worker()
        self.data['service_name']: str = get_package_root()
        self.data['config_dir']: Path = Path(self.params.config_dir).expanduser() / self.data['service_name']
        self.data['config_dir'].mkdir(parents=True, exist_ok=True)
        self.data['aws_dir']: Path = Path(self.params.aws_dir).expanduser()
        self.data['aws_dir'].mkdir(parents=True, exist_ok=True)
        self.data['credentials'] = self.data['aws_dir'] / 'credentials'
        self.data['credentials'].touch(exist_ok=True)

    def build_site_worker(self) -> SiteWorker:
        return SiteWorker(common_params=CommonParams(config_dir=self.params.config_dir), service_params=SiteParams())

    def read_profiles(self, domain: str, base_name: str = 'profiles.ini') -> Iterator[Profile]:
        profile_path: Path = self.data['config_dir'] / domain / base_name
        config = read_config(path=profile_path)
        for section in config.sections():
            role_tuple = RoleTuple(role_arn=config[section]['role_arn'], principle_arn=config[section]['principle_arn'])
            profile = Profile(name=section, role_tuple=role_tuple)
            yield profile

    @register_action('default')
    def main(self):
        domain: str = self.params.domain
        username: str = self.params.username
        password: str = self.params.password
        interactive: bool = bool(self.params.interactive)
        region: str = self.params.region
        profile: str = self.params.profile

        assertion = make_saml(domain, username, password)
        if not assertion:
            raise ValueError("Failed to retrieve SAML assertion")

        for role_tuple in iter_roles(assertion):
            credentials = assume_role(role_tuple, assertion, region)
            self.write_credentials(profile, credentials)

    def write_credentials(self, profile: str, credentials: Credentials):
        config = read_config(self.data['credentials'])
        if not config.has_section(profile):
            config.add_section(profile)
        config.set(profile, 'aws_access_key_id', credentials.access_key_id)
        config.set(profile, 'aws_secret_access_key', credentials.secret_access_key)
        config.set(profile, 'aws_session_token', credentials.session_token)
        config.set(profile, 'expiration', credentials.expiration.isoformat())
        write_config(self.data['credentials'], config)
