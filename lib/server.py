import requests
import hashlib
import uuid
import xmltodict
from os import makedirs
import os.path
from pathlib import Path

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

    def endpoint(self, endpoint, queries={}):
        q = ""
        for key, value in queries.items():
            q += f"&{key}={value}"

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
        self.online = self.handle_response(response)["valid"]
        return self.online

    def get_playlists(self):
        response = self.endpoint("rest/getPlaylists")
        return self.handle_response(response)["response"]

    def get_playlist(self, id):
        response = self.endpoint("rest/getPlaylist", {"id": id})
        return self.handle_response(response)["response"]

    def get_albums(self):
        response = self.endpoint("rest/getAlbumList", {"type": "newest", "size": 500})
        return self.handle_response(response)["response"]

    def get_album(self, id):
        print(f"get_album: {id}")
        return self.handle_response(response)["response"]

    def download(self, id, path):
        url = f"{self.address}/rest/download{self.get_queries()}&id={id}&format=mp3"
        response = requests.get(url)

        if response.headers["Content-Type"] == "text/xml":
            self.logger.error("Server Error while downloading song:")
            content = xmltodict.parse(response.content)
            self.logger.error(
                f"{content['subsonic-response']['error']['@code']}: {content['subsonic-response']['error']['@message']}"
            )
        else:  # must be binary data
            file = Path(path)
            file.parent.mkdir(exist_ok=True, parents=True)
            file.write_bytes(response.content)
