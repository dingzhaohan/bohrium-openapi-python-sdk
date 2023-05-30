
from client import Client
from image import Image
from job import Job
from storage import Storage
from project import Project
from util import Util
from node import Node
import os

def test_image():
    c = Client()
    c.login()
    i = Image(c)
    res = i.list_image_by_page(project_id=154)
    #print(res["items"][0].keys())
    i.print_image(154)


def test_job():
    c = Client()
    # c.login()
    # print(c.token)
    # ak = c.generate_access_key("ak")
    # print(ak)
    j = Job(c)
    data = j.detail()
    #print(j.log(10009242))
    #print(j.list_by_page(job_group_id=2107148))
    #j.get_job_token(20087266)
    #print(a["items"][0].keys())

def test_node():
    c = Client()
    node = Node(c)
    node.print_node(154)
    # data = node.list_server(154)
    # print(data)
    # headers = data[0].keys()
    # print(list(headers))
    # headers = ['nodeName','ip','nodePwd','cpu','memory','imageName', "cost",  'spec', 'createTime', 'diskSize', 'device']
    # items = []
    # for i in data:
    #     tmp_data = []
    #     # tmp_data = list(i.values())
    #     for k in headers:
    #         tmp_data.append(i[k])
    #     #print(tmp_data)
    #     items.append(tmp_data)
    # u = Util()
    # u.nice_print_table(headers=headers, items=items)

def test_project():
    c = Client()
    c.login()
    p = Project(client=c)
    p.print_project()

def test_storage():
    c = Client()
    j = Job(client=c)
    s = Storage(client = c)

    resp = j.create(project_id=154, name="upload_test")
    file_path = "/Users/dingzhaohan/Desktop/bohrium-openapi-python-sdk/bohriumsdk/client.py"
    file_name = os.path.basename(file_path)
    token = resp["token"]
    object_key = os.path.join(resp["storePath"], file_name)
    res = s.upload_from_file(object_key=object_key, file_path=file_path, token=token)

    # filename = "a.txt"
    # object_key = os.path.join(resp["storePath"], filename)
    # 
    # print(resp)
    # param = Parameter()
    # param.userMeta = {
    #         "a": "b",
    #         "ever":"17"
    #     }
    # param.contentType = "text/plain"
    # param.contentDisposition = f"attachment; filename={filename}"
    # param.filename = filename
    # res = s.write(object_key=object_key, data="1231231231231", token=token, parameter=param)
    # print(res)

    res = s.read(object_key=res["path"], token=token)
    print(res)