from model.config.Config import Config
from model.config.PlexPlaylistItem import PlexPlaylistItem
import toml
from os import path


class ConfigParser(object):
    def __init__(self, config_path) -> None:
        self.config_path = config_path

    def get_config_path(self):
        return self.config_path

    def set_config_path(self, config_path):
        self.config_path = config_path

    def get_parsed_toml_dict(self):
        return toml.load(self.config_path)

    # Returns a Config model
    def parse_config_file(self) -> Config:
        if not path.exists(self.config_path):
            # create an empty config file
            pass

        parsed_toml = self.get_parsed_toml_dict()
        config = Config()
        config.set_plex_api_token(parsed_toml["plex"]["plex_api_token"])
        config.set_plex_base_url(parsed_toml["plex"]["plex_base_url"])
        plex_playlist_items = []
        for playlist in parsed_toml["plex_playlist"]:
            for playlist_item in playlist["list"]:
                plex_playlist_item = PlexPlaylistItem()
                plex_playlist_item.set_playlist_name(
                    playlist_item["plex_playlist_name"]
                )
                plex_playlist_item.set_external_list_source(
                    playlist_item["external_list_source"]
                )
                plex_playlist_item.set_external_list_ids(
                    playlist_item["external_list_ids"]
                )
                plex_playlist_items.append(plex_playlist_item)
        config.set_playlist_items(plex_playlist_items)
        return config
