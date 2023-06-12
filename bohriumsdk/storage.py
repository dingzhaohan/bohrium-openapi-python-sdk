
from bohriumsdk.client import Client
from bohriumsdk.job import Job
import requests
import json
import base64
import os
from tqdm import tqdm

_DEFAULT_CHUNK_SIZE = 50 * 1024 * 1024
_DEFAULT_ITERATE_MAX_OBJECTS = 50
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
        self.host = "https://tiefblue.dp.tech"
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
        print(param)
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
        with open(file_path, 'rb') as fp:
            res = self.write(object_key=object_key, data=fp.read(), token=token, parameter=parameter)
            return res
    
    

    def init_upload_by_part(self, object_key: str, parameter=None):
        data = {
            'path': object_key
        }
        if parameter is not None:
            data['option'] = parameter.__dict__

        url = f"/api/upload/multipart/init"
        resp = self.client.post(url=url, host=self.host, data=data)
        return resp
    
    def upload_by_part(self, object_key: str, initial_key: str, chunk_size: int, number: int, body):
        param = {
            'initialKey': initial_key,
            'number': number,
            'partSize': chunk_size,
            'objectKey': object_key
        }
        headers = {}
        headers[self.TIEFBLUE_HEADER_KEY] = self._dump_parameter(param)
        url = f"/api/upload/multipart/upload"
        resp = self.client.post(url=url, host=self.host, data=body, headers=headers)
        return resp


    def complete_upload_by_part(self, object_key, initial_key, part_string):
        data = {
            'path': object_key,
            'initialKey': initial_key,
            'partString': part_string
        }

        url = f"/api/upload/multipart/complete"
        resp = self.client.post(url=url, host=self.host, data=data)
        return resp
    
    def upload_From_file_multi_part(
            self,
            object_key: str,
            file_path: str,
            token: str,
            chunk_size: int = _DEFAULT_CHUNK_SIZE,
            parameter = None,
            progress_bar = False,
            need_parse = False
        ) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError
        if os.path.isdir(file_path):
            raise IsADirectoryError
        if need_parse:
            _, _, object_key = self._parse_ap_name_and_tag(object_key)
        size = os.path.getsize(file_path)
        _, disposition = os.path.split(file_path)
        if parameter is None:
            parameter = Parameter()
        parameter.contentDisposition = f'attachment; filename="{disposition}"'
        bar_format = "{l_bar}{bar}| {n:.02f}/{total:.02f} %  [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
        with open(file_path, 'r') as f:
            pbar = tqdm(total=100, desc=f"Uploading {disposition}", smoothing=0.01, bar_format=bar_format,
                        disable=not progress_bar)
            f.seek(0)
            if size < _DEFAULT_CHUNK_SIZE * 2:
                print(object_key)
                self.write(object_key=object_key, token=token, data=f.buffer, parameter=parameter)
                pbar.update(100)
                pbar.close()
                return
            chunks = split_size_by_part_size(size, chunk_size)
            initial_key = self.init_upload_by_part(object_key, parameter).get('initialKey')
            part_string = []
            for c in chunks:
                f.seek(c.Offset)
                num_to_upload = min(chunk_size, size - c.Offset)
                part_string.append(self.upload_by_part(object_key, initial_key, chunk_size=c.Size, number=c.Number,
                                                       body=f.buffer.read(c.Size)).get('partString'))
                percent = num_to_upload * 100 / (size + 1)
                pbar.update(percent)
            pbar.close()
            return self.complete_upload_by_part(object_key, initial_key, part_string)

    def download_from_file(self):

        data = self.client.get()


    def _dump_parameter(self, parameter):
        j = json.dumps(parameter)
        return base64.b64encode(j.encode()).decode()
    
    def decode_base64(self, encode_data):
        data = json.loads(base64.b64decode(encode_data).decode('utf-8'))
        return data

    def _parse_ap_name_and_tag(self, input_path: str):
        l = input_path.split('/')
        if len(l) < 3:
            return "", "". l
        return l[0], l[1], "/".join(l[2:])



class Chunk:
    Number: int
    Offset: int
    Size: int
   
def split_size_by_part_size(total_size: int, chunk_size: int):
    if chunk_size < _DEFAULT_CHUNK_SIZE:
        chunk_size = _DEFAULT_CHUNK_SIZE
    chunk_number = int(total_size / chunk_size)
    if chunk_number >= 10000:
        raise TooManyChunk
    chunks = []
    for i in range(chunk_number):
        c = Chunk()
        c.Number = i + 1
        c.Offset = i * chunk_size
        c.Size = chunk_size
        chunks.append(c)

    if total_size % chunk_size > 0:
        c = Chunk()
        c.Number = len(chunks) + 1
        c.Offset = len(chunks) * chunk_size
        c.Size = total_size % chunk_size
        chunks.append(c)
    return chunks


def partial_with_start_from(start_bytes):
    return f'bytes={start_bytes}-'


def partial_with_end_from(end_bytes):
    return f'bytes=-{end_bytes}'


def partial_with_range(start_bytes, end_bytes):
    return f'bytes={start_bytes}-{end_bytes}'


TooManyChunk = Exception("too many chunks, please consider increase your chunk size")
