import sys
import os
import time
import base64, hashlib, hmac
import json
import requests


class Client:
    api_host = "https://openapi.samsungsdscloud.com"
    client_type = "OpenApi"
    def __init__(self, project_id: str = None, access_key: str = None, secret_key: str = None):
        self.method = ""
        self.path = ""

        try:
            if project_id is not None:
                self.project_id = project_id
            else:
                self.project_id = Client._read_config()['project-id']
            if access_key is not None:
                self.access_key = access_key
            else:
                self.access_key = Client._read_credentials()['access-key']
            if secret_key is not None:
                self.secret_key=secret_key
            else:
                self.secret_key = Client._read_credentials()['secret-key']
        except:
            sys.stderr.write("Required value not found.\n")
            sys.exit(1)

    def call_api(self, query: dict = None, body: dict = None):
        url = self._make_path(query=query)
        headers = self._make_header(url=url)
        response = requests.request(method=self.method, url=url, headers=headers, json=body)
        return response

    def set_method(self, method: str):
        self.method = method

    def set_path(self, path: str):
        self.path = path

    @staticmethod
    def _read_config():
        config_dir = os.path.expanduser(os.path.join('~', '.scp'))
        config_file = os.path.expanduser(os.path.join(config_dir, 'config.json'))

        try:
            with open(config_file, 'r') as file:
                config_values = json.load(file)
        except:
            sys.stdout.write("Invalid Configuration\n")
            sys.exit(1)
        return config_values

    @staticmethod
    def _read_credentials():
        credential_dir = os.path.expanduser(os.path.join('~', '.scp'))
        credential_file = os.path.expanduser(os.path.join(credential_dir, 'credentials.json'))

        try:
            with open(credential_file, 'r') as file:
                credential_values = json.load(file)
        except:
            sys.stdout.write("Invalid Credentials\n")
            sys.exit(1)
        return credential_values

    def _make_path(self, query: dict):
        query_string = ''
        if query is None:
            return self.api_host + self.path
        if len(query) == 0:
            return self.api_host + self.path
        query_string = query_string + "?"
        count = 0
        for key, value in query.items():
            count = count + 1
            query_string = query_string + key + "=" + value
            if len(query) > count:
                query_string = query_string + "&"
        path_string = self.api_host + self.path + query_string
        return path_string

    def _make_header(self, url):
        timestamp = str(int(time.time() * 1000))
        message = self.method + url + timestamp + self.access_key + self.project_id + self.client_type
        encoded_secret_key = bytes(self.secret_key, 'UTF-8')
        byte_string = bytes(message, 'UTF-8')
        string_hmac = hmac.new(encoded_secret_key, byte_string, digestmod=hashlib.sha256).digest()
        string_base64 = base64.b64encode(string_hmac).decode()
        header = {
            'X-Cmp-AccessKey': self.access_key,
            'X-Cmp-Signature': string_base64,
            'X-Cmp-Timestamp': timestamp,
            'X-Cmp-ClientType': self.client_type,
            'X-Cmp-ProjectId': self.project_id
        }
        return dict(header)


class EnterpriseClient(Client):
    api_host = "https://openapi.samsungsdscloud.com"
    client_type = "OpenApi"


class SamsungClient(Client):
    api_host = "https://sopenapi.samsungsdscloud.com"
    client_type = "OpenApi"
