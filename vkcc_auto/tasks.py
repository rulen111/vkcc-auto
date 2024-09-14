import os
import time
from io import BytesIO
from typing import IO

import requests
from celery import shared_task
from celery.exceptions import TaskError
from celery.utils.log import get_task_logger
from werkzeug.datastructures import FileStorage

from vkcc_auto.src.vkclient import VKclient
from vkcc_auto.src.wbhandler import WBHandler


@shared_task(bind=True)
def payload(
        self, input_file: str | os.PathLike | IO | bytes, filename: str,
        client_token: str, first_row: int = 2, input_col: int = 1, target_col: int = 2, rps_rate: int = 6
) -> object:
    if first_row < 1 or input_col < 1 or target_col < 1:
        raise TaskError(ValueError("Workbook index must be equal or greater than 1"))

    try:
        client = VKclient(client_token)
        client.test_request()

        wb = WBHandler(BytesIO(input_file))

        if first_row > 1:
            wb.write_header(first_row - 1, target_col)

        with requests.session() as session:
            max_row = wb.calc_max_row()
            for row in range(first_row, max_row + 1):
                link = wb.get_value(row, input_col)
                if not link:
                    break

                error, short_link = client.get_short_link(link, session=session)
                if error:
                    short_link = error.get("error_msg", "")

                wb.write_value(row, target_col, short_link)

                self.update_state(state='PROGRESS',
                                  meta={'current': row,
                                        'total': max_row})
                time.sleep(1 / rps_rate)
    except Exception as e:
        raise TaskError(e)

    virtual_workbook = BytesIO()
    wb.save(virtual_workbook)
    virtual_workbook.seek(0)
    result = virtual_workbook.read()

    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': result, "filename": filename}
