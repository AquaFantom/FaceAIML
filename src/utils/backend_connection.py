import requests
import json

class Backend:

    def __init__(self, base_url, root_password):
        self.base_url = base_url

        data = {
            'login': 'root',
            'password': root_password
        }
        data_json = json.dumps(data)
        r = requests.post(f'{base_url}/auth/login', data=data_json)
        self.cookies = r.cookies
        if r.json()['resultCode'] != 1000:
            raise Exception("Ошибка аунтификации")

    def _auth(self):
        r = requests.get(f'{self.base_url}/auth', cookies=self.cookies)
        result_code = r.json()['resultCode']
        return result_code == 1000

    def notify_access_log(self, is_access: bool = True):
        """
        Уведомляет backend о добавлении записи в AccessLogs
        """
        data = {
            'isAccess': is_access
        }
        data_json = json.dumps(data)
        r = requests.post(f'{self.base_url}/accessLog', data=data_json, cookies=self.cookies)
        if r.status_code != 200: return False
        result_code = r.json()['resultCode']
        if result_code == 3:
            if self._auth():
                r = requests.post(f'{self.base_url}/accessLog', data=data_json, cookies=self.cookies)
                if r.status_code != 200: return False
        return r.json()['resultCode'] == 0
