import requests
# import pylightxl as xl
from openpyxl import load_workbook


class VKclient(object):
    """Defining a custom VK client to work with API requests.
    Contains an access token and a method for getting a specific photo album."""
    def __init__(self, access_token, version="5.199"):
        self.token = access_token
        self.version = version
        self.params = {
            "access_token": self.token,
            "v": self.version,
        }

    def get_short_link(self, url, private=0):
        """"""
        baseurl = "https://api.vk.com/method/utils.getShortLink"
        params = {
            "url": url,
            "private": private,
        }

        # logging.info(f"User-{self.id}. Trying to get album '{album_id}'")
        response = requests.get(baseurl, params={**self.params, **params})

        return response.json().get("response", {})


def process_file(fp):
    wb = load_workbook(filename=fp, read_only=True)
    ws = wb.active
    for row in ws.values:
         print(row)



client = VKclient(token)
# response = client.get_short_link("https://dzen.ru/")
# print(response)
process_file(fp="input_example.xlsx")
