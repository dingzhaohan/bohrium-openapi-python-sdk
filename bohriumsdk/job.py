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
        params['accessKey'] = self.client.accesskey
        data = self.client.get(f'/openapi/v1/job/list', params=params)
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
        data = self.client.post(f"/openapi/v1/job/del/{job_id}", params=self.client.params)
        return data
    
    def terminate(self, job_id):
        data = self.client.post(f'/openapi/v1/job/terminate/{job_id}', params=self.client.params)
        return data
    
    def kill(self, job_id):
        data = self.client.post(f'/openapi/v1/job/kill/{job_id}', params=self.client.params)
        return data
    
    def log(self, job_id):
        data = self.client.get(f'/openapi/v1/job/{job_id}/log', params=self.client.params)
        return data

    def insert(self, **kwargs):
        must_fill = ['oss_path', 'project_id', 'machine_type', 'command', 'platform', 'image_address']
        # must_fill = ['job_type', 'oss_path', 'project_id', 'scass_type', 'command', 'platform', 'image_name']
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
        data = self.client.post(f"/openapi/v2/job/add", data=camel_data, params=self.client.params)
        return data


    def detail(self, job_id):
        data = self.client.get(f'/openapi/v1/job/{job_id}', params=self.client.params)
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
            data = self.client.post(f'/openapi/v1/job/create', data=data, params=self.client.params)
        except Exception as e:
            raise e
        return data
    
    def get_job_token(self, job_id):
        url = f"https://bohrium.dp.tech/brm/v1/job/{job_id}/input/token"
        headers = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODc0ODIwOTYsImlkZW50aXR5Ijp7Im9yZ0lkIjoxNTcsInVzZXJJZCI6MTU3fSwib3JpZ19pYXQiOjE2ODQ4OTAwOTZ9.g5aMIwQfWAhKMIxMptOE4jsz94OvQ1pKgigYI5VktC8akj9XnBl3PBBie_NETmqAhIRMmHuD7rEXIn-8U_SKQt3kdPj2i6q6opGzw8VOh4Wt5sBLjXZtZ_gdDPqD4YOM-khySMv_hYtK7yqJ-okmzcwVWIjH7GH-Yq09FY-tq8uZ2EDUwRlWsV0JFunSXqtDpH7zjj_kwbxPUjfH-DfTkX9cnhOLymFWVkdgsT4xJDgE8xCMvSUEk-1MRqW2GcQf3CZ3cNAAyQI1XSMEZtOBcHMZ14V-zOGTytgO2Y940R-RcC4ErBIKB_VMqvCWgDUumVexoe8z-0i8eGZ4b3knWA"
        }
        data = self.client.get(url=url, headers=headers)
        print(data)

if __name__ == "__main__":
    c = client.Client()
    j = Job(c)
    j.get_job_token(4711474)
