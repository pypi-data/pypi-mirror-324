import sys
import os
import time
import base64, hashlib, hmac
import json
import requests


api_host = "https://openapi.samsungsdscloud.com"
client_type = "OpenApi"


class Client:
    def __init__(self, project_id: str = None, access_key: str = None, secret_key: str = None):
        try:
            if project_id is not None:
                self.project_id = project_id
            else:
                self.project_id = Client.read_config()['project-id']
            if access_key is not None:
                self.access_key = access_key
            else:
                self.access_key = Client.read_credential()['access-key']
            if secret_key is not None:
                self.secret_key=secret_key
            else:
                self.secret_key = Client.read_credential()['secret-key']
        except:
            sys.stderr.write("Required value not found.\n")
            sys.exit(1)

    def invoke(self, query: dict = None, body: dict = None):
        url = Client.make_path(path=self.path, query=query)
        headers = Client.make_header(method=self.method, url=url, project_id=self.project_id,
                                        access_key=self.access_key, secret_key=self.secret_key)
        response = requests.request(method=self.method, url=url, headers=headers, json=body)
        return response

    def set_method(self, method: str):
        self.method = method

    def set_path(self, path: str):
        self.path = path

    @staticmethod
    def read_config():
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
    def read_credential():
        credential_dir = os.path.expanduser(os.path.join('~', '.scp'))
        credential_file = os.path.expanduser(os.path.join(credential_dir, 'credentials.json'))

        try:
            with open(credential_file, 'r') as file:
                credential_values = json.load(file)
        except:
            sys.stdout.write("Invalid Credentials\n")
            sys.exit(1)
        return credential_values

    @staticmethod
    def make_path(path: str, query: dict):
        query_string = ''
        if query is None:
            return api_host + path
        if len(query) == 0:
            return api_host + path
        query_string = query_string + "?"
        count = 0
        for key, value in query.items():
            count = count + 1
            query_string = query_string + key + "=" + value
            if len(query) > count:
                query_string = query_string + "&"
        path_string = api_host + path + query_string
        return path_string

    @staticmethod
    def make_header(method, url, project_id, access_key, secret_key):
        timestamp = str(int(time.time() * 1000))
        message = method + url + timestamp + access_key + project_id + client_type
        encoded_secret_key = bytes(secret_key, 'UTF-8')
        byte_string = bytes(message, 'UTF-8')
        string_hmac = hmac.new(encoded_secret_key, byte_string, digestmod=hashlib.sha256).digest()
        string_base64 = base64.b64encode(string_hmac).decode()
        header = {
            'X-Cmp-AccessKey': access_key,
            'X-Cmp-Signature': string_base64,
            'X-Cmp-Timestamp': timestamp,
            'X-Cmp-ClientType': client_type,
            'X-Cmp-ProjectId': project_id
        }
        return dict(header)
