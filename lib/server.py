import requests
import hashlib
import uuid
import xmltodict


class Server:
    def __init__(self, address, username, password, app_name):
        self.address = address
        self.username = username
        self.password = password
        self.app_name = app_name
        self.api_version = "1.16.1"

        self.salt = str(uuid.uuid4())[:6]
        self.token = hashlib.md5(f"{self.password}{self.salt}".encode()).hexdigest()

        print(self.ping())

    def ping(self):
        # todo make a function that returns all the obligatory search queries
        url = f"{self.address}/rest/ping.view?u={self.username}&t={self.token}&s={self.salt}&c={self.app_name}&v={self.api_version}"
        request = requests.get(url)
        response = xmltodict.parse(request.content)

        if response["subsonic-response"]["@status"] == "ok":
            return True
        elif response["subsonic-response"]["@status"] == "failed":
            # todo make logger work
            return False
        else:
            # todo make logger work. ts unexpected response from server
            return False
