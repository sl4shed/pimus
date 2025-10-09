import requests
import hashlib
import uuid
import xmltodict

from lib.logger import Logger


class Server:
    def __init__(self, address, username, password, app_name, logger: Logger):
        self.address = address
        self.username = username
        self.password = password
        self.app_name = app_name
        self.api_version = "1.16.1"
        self.logger = logger

    def get_queries(self):
        salt = str(uuid.uuid4())[:6]
        token = hashlib.md5(f"{self.password}{salt}".encode()).hexdigest()

        return f"?u={self.username}&t={token}&s={salt}&c={self.app_name}&v={self.api_version}"

    def endpoint(self, endpoint, queries=[]):
        q = ""
        for query in queries:
            q += f"?{query.key}={query.value}"
        url = f"{self.address}/{endpoint}{self.get_queries()}{q}"
        request = requests.get(url)
        return xmltodict.parse(request.content)

    def ping(self):
        response = self.endpoint("rest/ping.view")

        if response["subsonic-response"]["@status"] == "ok":
            return True
        elif response["subsonic-response"]["@status"] == "failed":
            self.logger.error(f"Server ping error:")
            self.logger.error(
                f"{response['subsonic-response']['error']['@code']}: {response['subsonic-response']['error']['@message']}"
            )
            return False
        else:
            self.logger.error("Unexpected response from server ping.")
            self.logger.error(response)
            return
