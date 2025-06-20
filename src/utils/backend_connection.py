import requests
import json

class Backend:

    def __init__(self, base_url):
        self.base_url = base_url

        data = {
            'login': 'admin',
            'password': 'admin'
        }
        data_json = json.dumps(data)
        r = requests.post(f'{base_url}/auth/login', data=data_json)
        self.cookies = r.cookies
        print(r.json())

    def post_access_log(self, employee_id: int, time: str, is_access: bool):
        data = {
            'employee_id': employee_id,
            'time': time,
            'access': is_access
        }
        data_json = json.dumps(data)
        r = requests.post(f'{self.base_url}/accessLog', data=data_json, cookies=self.cookies)
        if r.status_code != 200: return False
        return r.json()['resultCode'] == 100


backend = Backend("http://localhost:8000")
backend.post_access_log(1, '2025-12-12 12:25:10', True)