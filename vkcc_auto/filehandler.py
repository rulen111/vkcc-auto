from io import BytesIO

from flask import Blueprint, flash, redirect, render_template, request, send_file, current_app
from werkzeug.utils import secure_filename
from requests import RequestException

from .src import payload
from .src.utils import InvalidTokenError, WBReaderError, WBWriterError

bp = Blueprint("filehandler", __name__)


def allowed_file(filename: str | None) -> bool:
    """
    Check if a file is allowed
    :param filename: name of the file
    :return: True if allowed
    """
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() == "xlsx"


@bp.route("/", methods=("GET", "POST"))
def index():
    """
    The only route for this application. Displays file upload form.
    """
    if request.method == "POST":
        if "file" not in request.files:
            flash("Ошибка отправки файла", "Ошибка")

            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("Файл не выбран", "Ошибка")

            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            current_app.logger.info(f"Uploaded [{filename}]")

            token = current_app.config["TOKEN"]
            first_row = current_app.config["PAYLOAD_FIRST_ROW"]
            input_col = current_app.config["PAYLOAD_INPUT_COL"]
            target_col = current_app.config["PAYLOAD_TARGET_COL"]
            rps_rate = current_app.config["API_RPS_RATE"]
            try:
                wb = payload(file, token, first_row, input_col, target_col, rps_rate)
            except ValueError as e:
                current_app.logger.error(f"Value error on workbook indexing\n{e}")
                flash("Недопустимый индекс ячейки", "Ошибка сервера")
                return redirect(request.url)

            except InvalidTokenError as e:
                current_app.logger.error(f"API Authentification error\n{e}")
                flash("Неверный токен", "Ошибка сервера")
                return redirect(request.url)

            except WBReaderError as e:
                current_app.logger.error(f"File reader error\n{e}")
                flash("Ошибка обработки файла", "Ошибка сервера")
                return redirect(request.url)

            except RequestException as e:
                current_app.logger.error(f"API request error\n{e}")
                flash("Ошбика запроса к VK API", "Ошибка сервера")
                return redirect(request.url)

            except WBWriterError as e:
                current_app.logger.error(f"Writing to file error\n{e}")
                flash("Ошбика записи файла", "Ошибка сервера")
                return redirect(request.url)

            else:
                current_app.logger.info("Payload finished, sending file")
                virtual_workbook = BytesIO()
                wb.save(virtual_workbook)
                virtual_workbook.seek(0)

                return send_file(virtual_workbook, as_attachment=True, download_name=f"vkcc_{filename}",
                                 mimetype="application/vnd.ms-excel")
        else:
            flash("Неверное расширение файла", "Ошибка")

            return redirect(request.url)

    return render_template("index.html")
