import base64
import json

import requests

from os import environ, path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding


class PasswordManager(object):

    def __init__(self, endpoint=environ.get('GSENHA_ENDPOINT'),
                user=environ.get('GSENHA_USER'), password=environ.get('GSENHA_PASS'),
                key=environ.get('GSENHA_KEY', environ.get('GSENHA_KEY_PATH')), verify=None):
        self._user = user
        self._password = password
        self._verify = verify
        self._rsa_verifier = self._load_key(key)
        self._headers = {
            'Content-Type': 'application/json'
        }
        self._gsenha_endpoint = endpoint
        self._token = self._get_token()

    def _load_key(self, gsenha_key):
        if gsenha_key:
            gsenha_key = self.__load_key_from_file(gsenha_key)
        
        try:
            return load_pem_private_key(
                data=gsenha_key.encode('ascii'),
                password=None,
                backend=default_backend()
            )
        except ValueError:
            raise Exception('Error on loading the key')

    def __load_key_from_file(self, key_path):
        if path.exists(key_path):
            with open(key_path) as opened_key:
                return opened_key.read()
        else:
            raise ValueError('Key File does not exist')

    def _get_token(self):
        token_response = requests.post(
            '{}/login'.format(self._gsenha_endpoint),
            headers=self._headers,
            data=json.dumps({
                    'username': self._user,
                    'password': self._password,
                }
            ),
            verify=self._verify
        )

        if token_response.ok:
            token_json = token_response.json()
            if token_json:
                return token_json.get('token')

    def _get_password(self, folder, name):
        headers = {
            'Authorization': 'Bearer {}'.format(self._token)
        }

        response = requests.post(
            '{}/search/password'.format(self._gsenha_endpoint),
            headers={**self._headers, **headers},
            data=json.dumps({
                    'folder': folder,
                    'name': name
                }
            ),
            verify=self._verify
        )
        
        password_json = response.json()
        if password_json.get('status') == 'success':
            return password_json.get('password')

    def _decrypt(self, value):
        raw_cipher_data = base64.b64decode(value)
        return str(self._rsa_verifier.decrypt(raw_cipher_data, padding.PKCS1v15()).decode('utf-8'))

    def get_passwords(self, folder, *names):
        return_passwords = dict()
        for name in names:
            password = self._get_password(folder, name)
            if password:
                return_passwords[name] = {
                    'url': self._decrypt(password['url']),
                    'login': self._decrypt(password['login']),
                    'password': self._decrypt(password['passwd']),
                    'description': self._decrypt(password['description']),
                }
        return return_passwords
