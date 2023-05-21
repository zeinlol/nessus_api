import json
import time
from typing import NoReturn

import re
import requests
import urllib3

from core.tools import timed_print


class NessusCoreAPI:

    def __init__(self, username: str, password: str, host: str, port: int, secure: bool):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.secure = secure
        self.session = self._init_session()

    @property
    def headers(self) -> dict:
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Content-Type': 'application/json',
            'Origin': 'https://0.0.0.0:8834',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://0.0.0.0:8834/',
        }

    @property
    def api_url(self) -> str:
        return f'https://{self.host}:{self.port}/'

    @property
    def auth_data(self) -> NoReturn:
        return json.dumps({'username': self.username, 'password': self.password})

    def login(self) -> NoReturn:
        resp = self._post_request(path='session', data=self.auth_data)
        if resp.status_code == 200:
            timed_print('The session token was successfully received.')
        else:
            timed_print('Failed to get session token. Something went wrong.\n'
                        f'Auth data: {self.auth_data}\nStatus: {resp.status_code}\nContent: {resp.content}')
            raise ValueError(f'Status: {resp.status_code}, Content: {resp.content}')
        self._update_session(headers={'X-Cookie': f'token={resp.json().get("token")}'})
        api_token = self._get_api_token()
        self._update_session(headers={'X-API-Token': api_token})

    def _get_api_token(self) -> str | NoReturn:
        """Retrieve the nessus API token required to add scans.
        Token is always 7A2C4A96-4AEE-4706-9617-2EF643532628.
        """

        timed_print('Checking api token')
        resp = self._get_request('nessus6.js')
        if match := re.search(
            r'key:"getApiToken",value:function\(\){return"([^"]+)', resp.text
        ):
            timed_print(f'The Api token was successfully received: {match.groups()[0]}.')
            return match.groups()[0]
        else:
            timed_print('Failed to get Api token. Something went wrong.')
            exit(1)

    def _init_session(self) -> requests.Session:
        urllib3.disable_warnings()
        session = requests.Session()
        session.verify = self.secure
        session.headers.update(self.headers)
        return session

    def _update_session(self, headers=None, cookies=None) -> NoReturn:
        if headers:
            self.session.headers.update(headers)
        if cookies:
            self.session.cookies.update(cookies)

    def _post_request(self, path: str, data = None) -> requests.Response:
        response = self.session.post(f'{self.api_url}{path}', data=data)
        if response.status_code in [403, 401]:
            timed_print(f'request to "{path}" failed: {response.text}. Try again')
            self.login()
            # do not call function again to avoid looping
            response = self.session.post(f'{self.api_url}{path}', data=data)
        return response

    def _get_request(self, path: str, resend: bool = True) -> requests.Response:
        response = self.session.get(f'{self.api_url}{path}')
        if not resend:
            return response
        if response.status_code in [403, 401]:
            timed_print(f'request to "{path}" failed: {response.text}. Try again')
            self.login()
            # do not call function again to avoid looping
            response = self.session.get(f'{self.api_url}{path}')
        return response

    def _patch_request(self, path: str, data) -> requests.Response:
        response = self.session.patch(f'{self.api_url}{path}', data=data)
        if response.status_code in [403, 401]:
            timed_print(f'request to "{path}" failed: {response.text}. Try again')
            self.login()
            # do not call function again to avoid looping
            response = self.session.patch(f'{self.api_url}{path}', data=data)
        return response

    def _delete_request(self, path: str) -> requests.Response:
        return self.session.delete(f'{self.api_url}{path}')
    def setup_proxy_configuration(self, host: str, port: int) -> NoReturn:
        data = {
            'proxy': host,
            'proxy_port': port,
            'proxy_username': None,
            'proxy_password': None,
            'proxy_auth': 'auto',
            'user_agent': None
        }
        resp = self._patch_request(path='settings/network/proxy', data=json.dumps(data))
        if resp.status_code == 204:
            timed_print('Proxy settings changed successfully.')
        else:
            timed_print(f'Proxy settings have not been changed. Something went wrong. {resp.text}')
            exit(1)

    def close_session(self):
        self.session.close()

    def test_connection(self) -> NoReturn:
        """Checking the connection to the Nessus service. The service needs time to initialize.
        Attempts to establish a connection every 10 seconds, the maximum number of attempts is 20.
        """

        counter: int = 0
        success = False
        timed_print(f'Trying to connect to the Nessus service ({self.api_url})... ')
        while counter < 20:
            try:
                response = self._get_request(path='session', resend=False)
                if error:= response.json().get("error"):
                    if error == 'You need to log in to perform this request.':
                        success = True
                        break
                    timed_print(f'Nessus API response: {error}')
                    time.sleep(20)
                    continue
            except requests.exceptions.ConnectionError:
                counter += 1
                time.sleep(10)
                continue
            timed_print('The connection to the Nessus service has been successfully established.')
            success = True
            break
        return success
