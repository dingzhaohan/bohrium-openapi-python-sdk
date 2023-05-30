
from bohriumsdk.client import Client
from bohriumsdk.job import Job
import requests
import json
import base64
import os

class Parameter(object):
    contentType: str
    contentEncoding: str
    contentLanguage: str
    contentDisposition: str
    cacheControl: str
    acl: str
    expires: str
    userMeta: dict
    predefinedMeta: str

class Storage:
    TIEFBLUE_HEADER_KEY = 'X-Storage-Param'

    def __init__(
            self,
            base_url: str = "https://openapi.dp.tech",
            client: Client = None,
        ) -> None:
        
        self.base_url = base_url
        self.host = "https://tiefblue.test.dp.tech"
        self.client = client
        pass
    
    def encode_base64(
            self, 
            parameter: dict = {}
        ) -> str:
        j = json.dumps(parameter)
        return base64.b64encode(j.encode()).decode()

    def write(
            self, 
            object_key: str = "", 
            token: str = "",
            data: str = "" , 
            parameter: dict = {}, 
            progress_bar: dict = {}
        ) -> dict:

        param = {
            "path": object_key,
            'option': parameter
        }

        if parameter:
            param["option"] = parameter.__dict__
        
        headers = {}
        headers[self.TIEFBLUE_HEADER_KEY] = self.encode_base64(param)
        headers['Authorization'] = "Bearer " + token

        # req = self.client.post(f"/api/upload/binary", data=body)
        url = f"/api/upload/binary"
        
        req = self.client.post(url=url, host=self.host, headers=headers, data=data)
        # req = requests.post("https://tiefblue.dp.tech/api/upload/binary", headers=headers, data=data)
        # self._raise_error(req)
        return req
    
    def read(
            self,
            object_key: str = "",
            token: str = "",
            ranges: str = ""
        ) -> None:

        url = f"/api/download/{object_key}"
        self.client.token = token
        res = self.client.get(url=url, host=self.host, stream=True)
        return res
    

    def upload_from_file(
            self,
            object_key: str = "",
            file_path: str = "",
            token: str = "",
            parameter: dict = None
        ) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError
        if os.path.isdir(file_path):
            raise IsADirectoryError
        _, disposition = os.path.split(file_path)
        if parameter is None:
            parameter = Parameter()
        parameter.contentDisposition = f'attachment; filename="{disposition}"'
        with open(file_path, 'r') as fp:
            res = self.write(object_key=object_key,data=fp.read(), token=token, parameter=parameter)
            return res
    
    def download_from_file(self):
        pass
