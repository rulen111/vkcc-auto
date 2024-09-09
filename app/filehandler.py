from io import BytesIO
from typing import IO
import os

import requests
from tqdm import tqdm
from flask import (
    Blueprint, flash, redirect, render_template, request, send_file
)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .src.vkclient import VKclient
from .src.wbhandler import WBHandler

ALLOWED_EXTENSIONS = {"xlsx"}


bp = Blueprint("filehandler", __name__)


def allowed_file(filename: str | None) -> bool:
    """
    Check if a file is allowed
    :param filename: name of the file
    :return: True if allowed
    """
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def payload(
        input_file: str | os.PathLike | IO | FileStorage, client_token: str,
        first_row: int = 2, input_col: int = 1, target_col: int = 2
) -> WBHandler:
    """
    Application core logic. Takes input_file and returns processed workbook
    :param input_file: excel workbook file or path
    :param client_token: vk api access token to authorize requests
    :param first_row: first row of a data table (starts from 1)
    :param input_col: index of a column with input links (starts from 1)
    :param target_col: index of a column to write new links to (starts from 1)
    :return: WBHandler object
    """
    client = VKclient(client_token)
    # TODO: Handle exception
    wb = WBHandler(input_file)

    if first_row > 1:
        wb.write_header(first_row - 1, target_col)

    with requests.session() as session:
        for row in tqdm(range(first_row, wb.max_row + 1), desc="Fetching data..."):
            link = wb.get_value(row, input_col)
            if not link:
                break

            # TODO: Handle exception
            short_link = client.get_short_link(link, session=session)

            wb.write_value(row, target_col, short_link)

    return wb


@bp.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")

            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")

            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            wb = payload(file, TOKEN)
            virtual_workbook = BytesIO()
            wb.save(virtual_workbook)
            virtual_workbook.seek(0)

            return send_file(virtual_workbook, as_attachment=True, download_name=f"short_{filename}",
                             mimetype="application/vnd.ms-excel")

    return render_template("index.html")
