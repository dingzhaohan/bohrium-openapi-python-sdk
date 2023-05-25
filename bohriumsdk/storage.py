
from client import Client
from job import Job
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
            body: str = "" , 
            parameter: dict = {}, 
            progress_bar: dict = {}
        ) -> dict:

        param = {
            "path": object_key,
            'option': parameter
        }

        if parameter:
            param["option"] = parameter.__dict__
        
        # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBLZXkiOiJib2hyIiwidGFnIjoiY2xvdWQiLCJyZXNvdXJjZXMiOlt7IlByZWZpeCI6IjE1Ny9qb2IvNDcxMTg5Mi9pbnB1dC8iLCJBY3Rpb24iOjE1fV0sInByZWRlZmluZWRNZXRhIjpudWxsLCJleHAiOjE2ODQ4OTUyODZ9.iZp2MLBmfr4oN8o2kdEzbzZJftPFuYefttDus4v5Hjk"
        headers = {}
        headers[self.TIEFBLUE_HEADER_KEY] = self.encode_base64(param)
        headers['Authorization'] = "Bearer " + token

        # req = self.client.post(f"/api/upload/binary", data=body)
        
        req = requests.post("https://tiefblue.dp.tech/api/upload/binary", headers=headers, data=body)
        # self._raise_error(req)
        return req.json()
    
    

if __name__ == "__main__":
    c = Client()
    j = Job(client=c)
    s = Storage(client = c)

    resp = j.create(project_id=12742, name="upload_test")

    filename = "a.txt"
    object_key = os.path.join(resp["storePath"], filename)
    token = resp["token"]
    print(resp)
    param = Parameter()
    param.userMeta = {
            "a": "b",
            "ever":"17"
        }
    param.contentType = "text/plain"
    param.contentDisposition = f"attachment; filename={filename}"
    param.filename = filename
    res = s.write(object_key=object_key, token=token, parameter=param)
    print(res)