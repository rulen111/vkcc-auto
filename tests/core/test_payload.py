import time

import pytest

from vkcc_auto.src import payload
from vkcc_auto.src.utils import WBReaderError, InvalidTokenError


def test_payload_inputfile(invalid_wb_file, app):
    with pytest.raises(WBReaderError):
        wb = payload(invalid_wb_file, app.config["TOKEN"])
    time.sleep(0.1)


def test_payload_clienttoken(valid_wb_file):
    with pytest.raises(InvalidTokenError):
        wb = payload(valid_wb_file, "1234")
    time.sleep(0.1)


def test_payload_index(valid_wb_file, app):
    with pytest.raises(ValueError):
        wb = payload(valid_wb_file, app.config["TOKEN"], first_row=0)
    time.sleep(0.1)

    with pytest.raises(ValueError):
        wb = payload(valid_wb_file, app.config["TOKEN"], input_col=-2)
    time.sleep(0.1)

    with pytest.raises(ValueError):
        wb = payload(valid_wb_file, app.config["TOKEN"], target_col=0)
    time.sleep(0.1)


def test_payload_noheader(valid_wb_file, app):
    wb = payload(valid_wb_file, app.config["TOKEN"], first_row=1)
    time.sleep(0.1)


def test_payload_valid(valid_params, app):
    wb = payload(valid_params, app.config["TOKEN"])
    time.sleep(0.1)
