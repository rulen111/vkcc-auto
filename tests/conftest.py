import pytest
from openpyxl import Workbook

from vkcc_auto import create_app
from vkcc_auto.src import WBHandler, VKclient


# FACTORY
# ---------------------------------------------------------------------
@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


# WBHANDLER
# ---------------------------------------------------------------------
@pytest.fixture(scope="session")
def valid_wb_file(tmp_path_factory):
    wb = Workbook()
    fn = tmp_path_factory.mktemp("data") / "valid_wb.xlsx"
    wb.save(fn)

    return fn


@pytest.fixture(scope="session")
def valid_wb(valid_wb_file):
    wb = WBHandler(valid_wb_file)
    ws = wb.active_ws

    data = {
        "A1": "Full link",
        "A2": "https://dzen.ru/",
        "A3": "not a link",
    }
    for k, v in data.items():
        ws[k] = v

    return wb, data


@pytest.fixture(scope="session")
def invalid_wb_file(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data") / "invalid_wb.txt"
    with open(fn, "w") as f:
        f.write("invalid wb file")

    return fn


# VKCLIENT
# ---------------------------------------------------------------------
@pytest.fixture()
def vkclientobj(app):
    return VKclient(app.config["TOKEN"])

@pytest.fixture()
def valid_link():
    link = {
        "full": "https://dzen.ru/",
        "short": "https://vk.cc/ciLWS6",
    }
    return link
