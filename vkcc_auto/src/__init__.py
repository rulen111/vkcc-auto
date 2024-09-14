# import os
# import time
# from typing import IO
#
# import requests
# from werkzeug.datastructures import FileStorage
#
# from .wbhandler import WBHandler
# from .vkclient import VKclient
#
#
# def payload(
#         input_file: str | os.PathLike | IO | FileStorage, client_token: str,
#         first_row: int = 2, input_col: int = 1, target_col: int = 2, rps_rate: int = 6
# ) -> WBHandler:
#     """
#     Application core logic. Takes input_file and returns processed workbook
#     :param input_file: excel workbook file or path
#     :param client_token: vk api access token to authorize requests
#     :param first_row: first row of a data table (starts from 1)
#     :param input_col: index of a column with input links (starts from 1)
#     :param target_col: index of a column to write new links to (starts from 1)
#     :param rps_rate: vk api requests per second limit
#     :return: WBHandler object
#     """
#     if first_row < 1 or input_col < 1 or target_col < 1:
#         raise ValueError("Workbook index must be equal or greater than 1")
#
#     client = VKclient(client_token)
#     client.test_request()
#
#     wb = WBHandler(input_file)
#
#     if first_row > 1:
#         wb.write_header(first_row - 1, target_col)
#
#     with requests.session() as session:
#         for row in range(first_row, wb.max_row + 1):
#             link = wb.get_value(row, input_col)
#             if not link:
#                 break
#
#             error, short_link = client.get_short_link(link, session=session)
#             if error:
#                 short_link = error.get("error_msg", "")
#
#             wb.write_value(row, target_col, short_link)
#             time.sleep(1 / rps_rate)
#
#     return wb
