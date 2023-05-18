import requests
import client
import humps

class Job:
    def __init__(self, client):
        self.client = client

    def list_by_page(self, job_group_id, status=None, page=1, per_page=50):
        params = {
            'groupId': job_group_id,
            'page': page,
            'pageSize': per_page
        }
        if status:
            params['status'] = status
        # print(self.client.access_key)
        data = self.client.get(f'/openapi/v1/job/list?accessKey={self.client.accesskey}', params=params)
        return data
    

    def list_by_number(self, job_group_id, number, status=None):
        if status is None:
            status = []
        per_page = 50
        job_list = []
        data = self.list_by_page(job_group_id, page=1, per_page=per_page, status=status)
        total = data.get("total")
        per_page = data.get("pageSize")
        page_number = 0
        while page_number * per_page < total:
            page_number = page_number + 1
            if page_number > 1:
                data = self.list_by_page(job_group_id, page_number, per_page, status)
            for each in data.get("items"):
                job_list.append(each)
                if number != -1 and len(job_list) >= number:
                    return job_list
        return job_list
    
    def delete(self, job_id):
        data = self.client.post(f"/openapi/v1/job/del/{job_id}?accessKey={self.client.access_key}")
        return data
    
    def terminate(self, job_id):
        data = self.client.post(f'/openapi/v1/job/terminate/{job_id}?accessKey={self.client.access_key}')
        return data
    
    def kill(self, job_id):
        data = self.client.post(f'/openapi/v1/job/kill/{job_id}?accessKey={self.client.access_key}')
        return data
    
    def log(self, job_id):
        data = self.client.get(f'/openapi/v1/job/{job_id}/log?accessKey={self.client.access_key}')
        return data

    def insert(self, **kwargs):
        must_fill = ['oss_path', 'project_id', 'machine_type', 'command', 'platform', 'image_address']
        must_fill = ['job_type', 'oss_path', 'project_id', 'scass_type', 'command', 'platform', 'image_name']
        for each in must_fill:
            if each not in kwargs:
                raise ValueError(f'{each} is required when submitting job')
        camel_data = {humps.camelize(k): v for k, v in kwargs.items()}
        if not isinstance(camel_data['ossPath'], list):
            camel_data['ossPath'] = [camel_data['ossPath']]
        if 'logFile' in camel_data:
            camel_data['logFiles'] = camel_data['logFile']
        if 'logFiles' in camel_data and not isinstance(camel_data['logFiles'], list):
            camel_data['logFiles'] = [camel_data['logFiles']]
        if self.client.debug:
            print(camel_data)
        data = self.client.post(f"/openapi/v2/job/add?accessKey={self.client.access_key}", data=camel_data)
        return data


    def detail(self, job_id):
        data = requests.get(f'/openapi/v1/job/{job_id}?accessKey={self.client.access_key}')
        return data
    
    def create(self, project_id, name='', group_id=0):
        data = {
            'projectId': project_id
        }
        if name:
            data['name'] = name
        if group_id:
            data['groupId'] = group_id
        try:
            data = self.client.post(f'/openapi/v1/job/create?accessKey={self.client.access_key}', data=data)
        except Exception as e:
            raise e
        return data
    

if __name__ == '__main__': 
    client = client.Client()
    #client.login()
    #client.generate_accesskey()
    client.accesskey = "c30c4ca1bf354404301cd892be0f5008"
    job = Job(client)
    
    # data = job.list_by_page(10781814)
    # print(data.json())

    data = job.detail(7160282)
    print(data.json())