import datetime

import requests
from datetime import datetime

class ULHandler:
    def __init__(self):
        self.token = None
        self.timetables = None

    def set_token(self, token:str):
        self.token = token

    def get_cached_timetable(self):
        return self.timetables

    def get_timetables(self, start:datetime, end:datetime):
        if self.timetables is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Content-Type': 'application/json',
                'Origin': 'https://mobile.univ-lorraine.fr',
                'Connection': 'keep-alive',
                'Referer': 'https://mobile.univ-lorraine.fr/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Priority': 'u=0',
            }

            json_data = {
                'authToken': self.token,
                'startDate': start.strftime("%Y-%m-%d"),
                'endDate': end.strftime("%Y-%m-%d"),
                'asUser': None,
            }

            response = requests.post('https://mobile-back.univ-lorraine.fr/schedule', headers=headers, json=json_data)
            self.timetables = response.json()
        return self.timetables

    def login_with_password(self, username, password):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/json',
            'Origin': 'https://mobile.univ-lorraine.fr',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Referer': 'https://mobile.univ-lorraine.fr/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Priority': 'u=0',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        json_data = {
            'username': username,
            'password': password,
        }

        response = requests.post('https://mobile-back.univ-lorraine.fr/auth', headers=headers, json=json_data)
        if "authToken" in response.json():
            self.token = response.json()["authToken"]
            return True
        else:
            return False