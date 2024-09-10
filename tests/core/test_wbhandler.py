import pytest

from openpyxl import Workbook

from vkcc_auto.src.utils import WBReaderError, WBWriterError
from vkcc_auto.src.wbhandler import WBHandler

COL_MAP = {"A": 1, "B": 2, }


def test_wbhandler(valid_wb_file):
    assert isinstance(WBHandler(valid_wb_file), WBHandler)
    assert isinstance(WBHandler(valid_wb_file).wb, Workbook)


def test_wbhandler_reader(invalid_wb_file):
    with pytest.raises(WBReaderError):
        WBHandler(invalid_wb_file)


def test_wbhandler_get_value(valid_wb):
    wb, data = valid_wb

    for k, v in data.items():
        assert wb.get_value(int(k[1]), COL_MAP[k[0]]) == v


def test_wbhandler_write_header(valid_wb):
    wb, data = valid_wb
    test_value = "TEST"
    wb.write_header(int("A1"[1]), COL_MAP["B1"[0]], value=test_value)

    assert wb.get_value(int("A1"[1]), COL_MAP["B1"[0]]) == test_value


def test_wbhandler_write_value(valid_wb):
    wb, data = valid_wb
    test_value = "TEST"
    wb.write_value(int("A2"[1]), COL_MAP["B2"[0]], test_value)

    assert wb.get_value(int("A2"[1]), COL_MAP["B2"[0]]) == test_value


def test_wbhandler_writer(valid_wb):
    with pytest.raises(WBWriterError):
        wb, data = valid_wb
        wb.save(wb)
