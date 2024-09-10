import pytest
import time
from requests import RequestException, Session

from vkcc_auto.src.utils import InvalidTokenError


def test_vkclient_test_request(vkclientobj):
    vkclientobj.test_request()
    time.sleep(0.1)


def test_vkclient_test_request_exc(vkclientobj):
    with pytest.raises(InvalidTokenError):
        vkclientobj.auth_params["access_token"] = "1234"
        vkclientobj.test_request()
    time.sleep(0.1)


def test_vkclient_get_short_link(vkclientobj, valid_link):
    base_url = vkclientobj.baseurl
    with pytest.raises(RequestException):
        vkclientobj.baseurl = "not a link"
        short_link = vkclientobj.get_short_link(valid_link["full"])
    time.sleep(0.1)

    vkclientobj.baseurl = base_url
    short_link = vkclientobj.get_short_link(valid_link["full"])
    assert short_link == valid_link["short"]
    time.sleep(0.1)

    session = Session()
    short_link = vkclientobj.get_short_link(valid_link["full"], session=session)
    assert short_link == valid_link["short"]
    time.sleep(0.1)

    short_link = vkclientobj.get_short_link("not a link")
    assert short_link == "One of the parameters specified was missing or invalid: invalid url"
    time.sleep(0.1)

    time.sleep(1)
