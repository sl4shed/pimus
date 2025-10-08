import requests
import hashlib
import uuid


class server:
    def __init__(self, address, username, password, app_name):
        self.address = address
        self.username = username
        self.password = password
        self.app_name = app_name
        self.api_version = "1.16.1"

        self.salt = str(uuid.uuid4())[:6]
        self.token = hashlib.md5(self.password + self.salt)

        self.ping()

    def ping(self):
        request = requests.get(
            f"{self.address}/rest/ping.view?u={self.username}&p={self.token}&c={self.app_name}&v={self.api_version}&s={self.salt}"
        )
        print(request.content)

        return request.content
