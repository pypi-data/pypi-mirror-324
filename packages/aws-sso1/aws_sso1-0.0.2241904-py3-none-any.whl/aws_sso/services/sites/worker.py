from ...abstract import AbstractService
from ...utils import get_package_root, read_config, register_action, write_config
from .model import SiteLogin
from configparser import ConfigParser
from pathlib import Path
from typing import Iterator, List, Optional
import getpass
import keyring


class SiteWorker(AbstractService):

    @classmethod
    def infer_domain(cls, domain: str) -> Optional[str]:
        delimiter: str = '.'
        parts: List[str] = domain.split(delimiter)
        if len(parts) > 1:
            return delimiter.join(parts[-2:])

    @classmethod
    def build_domain_username(cls, domain: str, username: str) -> str:
        delimiter: str = '\\'
        domain: str = cls.infer_domain(domain)
        parts: List[str] = [domain or '', username]
        return delimiter.join(parts).strip(delimiter)

    def initialize(self):
        self.data['service_name']: str = get_package_root()
        self.data['config_dir']: Path = Path(self.params.config_dir).expanduser() / self.data['service_name']
        self.data['config_dir'].mkdir(parents=True, exist_ok=True)
        self.data['sites_path']: Path = self.data['config_dir'] / 'sites.ini'

    def add_site(self, domain: str, username: str, password: str):
        domain_username: str = self.build_domain_username(domain, username)
        keyring.set_password(service_name=self.data['service_name'], username=domain_username, password=password)
        sites_path: Path = self.data['sites_path']
        config: ConfigParser = read_config(path=sites_path)
        if not config.has_section('sites'):
            config.add_section('sites')
        config.set('sites', domain, username)
        write_config(path=sites_path, config=config)

    def remove_site(self, domain: str):
        sites_path: Path = self.data['sites_path']
        config: ConfigParser = read_config(path=sites_path)
        if config.has_section('sites') and config.has_option('sites', domain):
            username = config.get('sites', domain)
            domain_username: str = self.build_domain_username(domain, username)
            keyring.delete_password(service_name=self.data['service_name'], username=domain_username)
            config.remove_option('sites', domain)
            write_config(path=sites_path, config=config)

    def list_sites(self) -> Iterator[str]:
        sites_path: Path = self.data['sites_path']
        config: ConfigParser = read_config(path=sites_path)
        if config.has_section('sites'):
            for domain in config.options('sites'):
                yield domain

    @register_action('add')
    def handle_add(self):
        domain: str = self.params.domain
        username: str = self.params.username
        password: str = self.params.password or getpass.getpass(prompt=f'Password for {username}@{domain}: ')
        self.add_site(domain, username, password)

    @register_action('remove')
    def handle_remove(self):
        domain: str = self.params.domain
        self.remove_site(domain)

    @register_action('list')
    def handle_list(self):
        for domain in self.list_sites():
            print(domain)
