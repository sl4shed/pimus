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
            q += f"?{query['key']}={query['value']}"
        url = f"{self.address}/{endpoint}{self.get_queries()}{q}"
        request = requests.get(url)
        return xmltodict.parse(request.content)

    def handle_response(self, response):
        if response["subsonic-response"]["@status"] == "ok":
            return {"valid": True, "response": response}
        elif response["subsonic-response"]["@status"] == "failed":
            self.logger.error(f"Server error:")
            self.logger.error(
                f"{response['subsonic-response']['error']['@code']}: {response['subsonic-response']['error']['@message']}"
            )
            return {"valid": False, "response": response}
        else:
            self.logger.error("Unexpected response from server:")
            self.logger.error(response)
            return {"valid": False, "response": response}

    def ping(self):
        response = self.endpoint("rest/ping.view")
        return self.handle_response(response)["valid"]

    def get_playlists(self):
        response = self.endpoint("rest/getPlaylists")
        return self.handle_response(response)["response"]

    def get_playlist(self, id):
        response = self.endpoint("rest/getPlaylist", [{"id": id}])
        return self.handle_response(response)["response"]
