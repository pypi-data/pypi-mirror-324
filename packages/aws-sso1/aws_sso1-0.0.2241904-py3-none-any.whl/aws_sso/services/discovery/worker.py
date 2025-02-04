from ...abstract import AbstractService
from ...model import CommonParams
from ..sites import *
from ...utils import get_package_root, read_config, register_action, write_config
from .core import part_1, part_2
from configparser import ConfigParser
import logging
from pathlib import Path
from typing import List, Union


class DiscoveryWorker(AbstractService):

    def build_site_worker(self) -> SiteWorker:
        return SiteWorker(common_params=CommonParams(config_dir=self.params.config_dir), service_params=SiteParams())

    def initialize(self):
        self.tools['sites'] = self.build_site_worker()
        self.data['service_name']: str = get_package_root()
        self.data['config_dir']: Path = Path(self.params.config_dir).expanduser() / self.data['service_name']
        self.data['config_dir'].mkdir(parents=True, exist_ok=True)

    def build_profile_path(self, domain: str, base_name: str = 'profiles.ini') -> Path:
        path: Path = self.data['config_dir'] / domain / base_name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        return path

    def discover(self, domain: str, skip_names: bool = True):
        site_login: SiteLogin = self.tools['sites'].get_site_login(domain)
        profile_path: Path = self.build_profile_path(domain=site_login.domain)
        config: ConfigParser = read_config(path=profile_path)

        idp_submit_url, payload = part_1(domain=site_login.domain, username=site_login.username, password=site_login.password)
        role_tuples = part_2(idp_submit_url, payload)

        for idx, role_tuple in enumerate(role_tuples):
            section_name = f'profile{idx + 1}' if skip_names else role_tuple.role_name
            if not config.has_section(section_name):
                config.add_section(section_name)
            config.set(section_name, 'role_arn', role_tuple.role_arn)
            config.set(section_name, 'principle_arn', role_tuple.principle_arn)

        write_config(path=profile_path, config=config)

    @register_action('discover')
    def main(self):
        self.discover(domain=self.params.domain, skip_names=bool(self.params.skip_names))
