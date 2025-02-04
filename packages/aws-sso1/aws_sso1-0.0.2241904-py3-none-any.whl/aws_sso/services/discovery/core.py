from ...utils import string_contains
from .model import RoleTuple

from bs4 import BeautifulSoup
from requests_ntlm import HttpNtlmAuth
from typing import Callable, Dict, Iterator, Optional
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import base64
import logging
import requests
import re


def part_1(domain: str, username: str, password: str, verify_ssl: bool = True):
    # TODO: use better function name
    session = requests.Session()
    session.auth = HttpNtlmAuth(username, password)
    idp_entry_url = build_idp_entry_url(domain)
    response = session.get(idp_entry_url, verify=verify_ssl)
    idp_submit_url = response.url
    logging.info('set idp url', extra=dict(entry=idp_entry_url, submit=idp_submit_url))
    payload = build_payload(response, username, password)
    logging.debug('payload', extra=payload)
    new_idp_submit_url = find_new_idp_submit_url(response, idp_entry_url)
    if new_idp_submit_url:
        old_idp_submit_url = idp_submit_url
        idp_submit_url = new_idp_submit_url
        logging.info('set idp url', extra=dict(urls=[idp_entry_url, old_idp_submit_url, idp_submit_url]))
    session.close()
    return idp_submit_url, payload


def build_payload(response, username: str, password: str) -> Dict:
    soup = BeautifulSoup(response.text, features='html5lib')
    process_tag = build_payload_tag_engine(username, password)
    return {tag.get('name'): process_tag(tag) for tag in soup.find_all(re.compile('input'))}


def build_payload_tag_engine(username: str, password: str) -> Callable:
    def process_tag(tag):
        if tag.get('name') == 'username':
            return username
        elif tag.get('name') == 'password':
            return password
        return tag.get('value', '')

    return process_tag


def build_idp_entry_url(domain: str) -> str:
    return f'https://{domain}/adfs/ls/IdpInitiatedSignOn.aspx'


def find_new_idp_submit_url(response, idp_entry_url: str) -> Optional[str]:
    soup = BeautifulSoup(response.text, features='html5lib')
    form = soup.find('form')
    if form and form.get('action'):
        parsed_url = urlparse(idp_entry_url)
        return f'{parsed_url.scheme}://{parsed_url.netloc}{form.get("action")}'
    return None


def part_2(idp_submit_url: str, payload: Dict[str, str], verify_ssl: bool = True) -> Iterator[RoleTuple]:
    # TODO: use better function name
    response = requests.post(url=idp_submit_url, data=payload, verify=verify_ssl)
    assertion = find_assertion(response)
    root = parse_assertion(assertion)
    return (RoleTuple.from_saml(data) for data in iter_saml_data(root))


def find_assertion(response) -> Optional[str]:
    soup = BeautifulSoup(response.text, features='html5lib')
    assertion = None
    for input_tag in soup.find_all('input'):
        if input_tag.get('name') == 'SAMLResponse':
            assertion = input_tag.get('value')
            break
    return assertion


def parse_assertion(assertion: str) -> ET.Element:
    decoded_assertion = base64.b64decode(assertion)
    return ET.fromstring(decoded_assertion)


def iter_saml_data(root: ET.Element) -> Iterator[Dict]:
    for attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
        data = {attr.get('Name'): attr.text for attr in attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue')}
        yield data
