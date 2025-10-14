import os.path


class Song:
    def __init__(self, info, config, server, logger):
        self.info = info
        self.server = server
        self.config = config
        self.logger = logger

        self.path = os.path.join(
            self.config.get("songs_folder"),
            self.info[
                "@path"
            ],  # this is the path that the song is stored on in the server, this way i guess you have the directory structure that you like
        )

        # metadata
        self.id = self.info["@id"]
        self.title = self.info["@title"]
        self.artist = self.info["@artist"]
        self.album = self.info["@album"]

        self.downloaded = os.path.exists(self.path)

    def download(self, force=False):
        if self.downloaded and not force:
            return

        self.logger.info(
            f"Downloading song {self.info['@title']} by {self.info['@artist']}"
        )
        self.server.download(self.info["@id"], self.path)
