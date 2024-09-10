import requests
from .utils import InvalidTokenError


class VKclient(object):
    """Defining a custom VK client to work with API requests.
    Contains an access token and a method for getting a short link."""
    def __init__(self, access_token: str = "", version: str = "5.199", token_type: str = "service") -> None:
        """
        Setting up authentication parameters
        :param access_token: an access token to authorize requests
        :param version: vk api version
        :param token_type: can be "user", "service" or "community".
        Private link metrics are provided only with "user" authorization
        """
        self.baseurl = "https://api.vk.com/method/utils.getShortLink"
        self.token_type = token_type
        self.auth_params = {
            "access_token": access_token,
            "v": version,
        }

    def test_request(self):
        params = {
            "url": "https://dzen.ru/",
            "private": 0,
        }
        # response = requests.get(self.baseurl, params={**self.auth_params, **params}, timeout=0.1)
        response = requests.get(self.baseurl, params={**self.auth_params, **params})
        response.raise_for_status()

        error = response.json().get("error", None)
        if error:
            raise InvalidTokenError()

    def get_short_link(self, url: str, private: int = 0, session: requests.Session = None) -> str:
        """
        Method for handling "utils.getShortLink" request
        :param url: a url to be shortened
        :param private: if link metrics should be private, either "0" (public) or "1" (private)
        :param session: requests "Session" object for single domain requests optimization. Optional
        :return: short link from vk.cc service
        """
        params = {
            "url": url,
            "private": private,
        }

        if session:
            # response = session.get(self.baseurl, params={**self.auth_params, **params}, timeout=0.1)
            response = session.get(self.baseurl, params={**self.auth_params, **params})
        else:
            # response = requests.get(self.baseurl, params={**self.auth_params, **params}, timeout=0.1)
            response = requests.get(self.baseurl, params={**self.auth_params, **params})
        response.raise_for_status()

        error = response.json().get("error", None)
        if error:
            return error.get("error_msg", "")

        return response.json().get("response", {}).get("short_url", "")
