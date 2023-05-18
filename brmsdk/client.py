import requests
import os
import json
import urllib
import getpass
import time
import configparser

class RequestInfoException(Exception):
    pass

class Client:
    def __init__(self, config_file_location='~/.brmconfig'):
        
        config_file_location_expand = os.path.expanduser(config_file_location)

        if not os.path.exists(config_file_location_expand):
            raise FileNotFoundError("Config File ~/.brmconfig not found!")
        config = configparser.ConfigParser()
        config.read(config_file_location_expand)
        self.base_url = config.get('Credentials', 'baseUrl')
        self.access_key = config.get('Credentials', 'accessKey')


    def post(self, url, data=None, headers=None, params=None, retry=5):
        return self._req('POST', url, data=data, headers=headers, params=params, retry=retry)

    def get(self, url, data=None, headers=None, params=None, retry=5):
        return self._req('GET', url, data=data, headers=headers, params=params, retry=retry)

    def _req(self, method, url, data=None, headers=None, params=None, retry=5):
        url = urllib.parse.urljoin(self.base_url, url)

        # Set Headers
        if headers is None: header = {}
        # if self.token: headers['Authorization'] = f'Bearer {self.token}'
        # headers['bohr-client'] = f'utility:0.0.2'
        resp_code = None
        for i in range(retry):
            resp = None
            err = ""
            if method == 'GET':
                resp = requests.get(url, params=params, headers=headers)
            if method == 'POST':
                resp = requests.post(url=url, json=data, params=params, headers=headers)
            resp_code = resp.status_code
            if not resp.ok:
                try:
                    result = resp.json()
                    err = result.get("error")
                except:
                    pass
                time.sleep(0.1 * i)
                continue
            result = resp.json()
            if result.get('model', '') == 'gpt-35-turbo':
                return result['choices'][0]['message']['content']
            elif result['code'] == 0:
                return result.get('data', {})
            else:
                err = result.get("message") or result.get("error")
                break
        raise RequestInfoException(resp_code, url, err)

    def get_token(self):
        self.login()
        return self.token


    def login(self):
        email = input("Please enter Bohrium Account Email: ")
        password = getpass.getpass(prompt="Please enter password: ")
        post_data = {
            'username': email,
            'password': password
        }
        resp = self.post('https://bohrium.dp.tech/account_gw/login', post_data)
        self.token = resp['token']
        print("Login successfully!")

    def generate_access_key(self, name="default"):
        post_data = {
            "name": name
        }
        resp = self.post(url="https://bohrium.dp.tech/bohrapi/v1/ak/add", data=post_data)
        self.acces_skey = resp["accessKey"]
        return resp


    def chat(self, prompt, temperature=0):
        post_data = {
            "messages":[{"role":"user","content":f"{prompt}"}],
            "stream":False,
            "model":"gpt-3.5-turbo",
            "temperature":temperature,
            "presence_penalty":0
        }
        
        resp = self.post(f"/openapi/v1/chat/complete?accessKey={self.access_key}", data=post_data)
        return resp

if __name__ == '__main__':
    c = Client()
    resp = c.chat("你好")
    print(resp)
    # config = configparser.ConfigParser()
    # config.read(os.path.expanduser("~/.brmconfig"))

    # base_url = config.get('Credentials', 'baseUrl')
    # access_key = config.get('Credentials', 'accessKey')
    # print('Base URL:', base_url)
    # print('Access Key:', access_key)