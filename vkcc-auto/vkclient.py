import requests


class VKclient(object):
    """Defining a custom VK client to work with API requests.
    Contains an access token and a method for getting a specific photo album."""

    def __init__(self, access_token="", version="5.199"):
        self.access_token = access_token
        self.version = version
        self.auth_params = {
            "access_token": self.access_token,
            "v": self.version,
        }

    def get_short_link(self, url: str):
        """"""
        baseurl = "https://api.vk.com/method/utils.getShortLink"
        params = {
            "url": url,
            "private": 0,
        }

        # logging.info(f"User-{self.id}. Trying to get album '{album_id}'")
        response = requests.get(baseurl, params={**self.auth_params, **params})

        return response.json().get("response", {}).get("short_url", "")
