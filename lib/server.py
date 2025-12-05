import hashlib
import json
import os.path
import uuid
from os import makedirs
from pathlib import Path

import requests
import xmltodict

from lib.logger import Logger


class Server:
    def __init__(self, address, username, password, app_name, logger):
        self.address = address
        self.username = username
        self.password = password
        self.app_name = app_name
        self.api_version = "1.16.1"
        self.logger = logger

        if not self.ping():
            print("plug")
            self.logger.broadcast("Server offline!")

    def get_queries(self):
        salt = str(uuid.uuid4())[:6]
        token = hashlib.md5(f"{self.password}{salt}".encode()).hexdigest()

        return f"?u={self.username}&t={token}&s={salt}&c={self.app_name}&v={self.api_version}"

    def cache_endpoint(self, endpoint, response, queries={}):
        if endpoint == "rest/ping.view":
            return
        with open("./cache/responses.json", "r") as file:
            responses = json.loads(file.read())
            if queries != {}:
                responses[f"{endpoint}+{json.dumps(queries)}"] = response
            else:
                responses[endpoint] = response
        with open("./cache/responses.json", "w") as file:
            file.write(json.dumps(responses))

    def get_cached_endpoint(self, endpoint, queries={}):
        with open("./cache/responses.json", "r") as file:
            responses = json.loads(file.read())
            if queries != {}:
                return responses[f"{endpoint}+{json.dumps(queries)}"]
            else:
                return responses[endpoint]

    def endpoint(self, endpoint, queries={}):
        if endpoint != "rest/ping.view" and not self.online:
            return self.get_cached_endpoint(endpoint, queries)

        q = ""
        for key, value in queries.items():
            q += f"&{key}={value}"

        url = f"{self.address}/{endpoint}{self.get_queries()}{q}"
        request = requests.get(url)
        response = xmltodict.parse(request.content)
        self.cache_endpoint(endpoint, response, queries)

        return response

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
        response = self.endpoint("rest/getAlbum", {"id": id})
        return self.handle_response(response)["response"]

    def get_artists(self):
        response = self.endpoint("rest/getArtists")
        return self.handle_response(response)["response"]

    def get_artist(self, id):
        response = self.endpoint("rest/getArtist", {"id": id})
        return self.handle_response(response)["response"]

    def get_top_songs(self, artist_name):
        response = self.endpoint("rest/getTopSongs", {"artist": artist_name})
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
