from io import BytesIO

from flask import Blueprint, flash, redirect, request, send_file, current_app, url_for, jsonify
from werkzeug.utils import secure_filename

from .src.utils import allowed_file
from . import tasks

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.post("/run")
def run():
    """
    The only route for this application. Displays file upload form.
    """
    if "file" not in request.files:
        flash("Ошибка отправки файла", "Ошибка")

        # return redirect(url_for("index"))
        return jsonify({'redirect': url_for('index')})

    file = request.files["file"]
    if file.filename == "":
        flash("Файл не выбран", "Ошибка")

        # return redirect(url_for("index"))
        return jsonify({'redirect': url_for('index')})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        current_app.logger.info(f"Uploaded [{filename}]")

        token = current_app.config["TOKEN"]
        first_row = current_app.config["PAYLOAD_FIRST_ROW"]
        input_col = current_app.config["PAYLOAD_INPUT_COL"]
        target_col = current_app.config["PAYLOAD_TARGET_COL"]
        rps_rate = current_app.config["API_RPS_RATE"]
        # try:
        task = tasks.payload.delay(file.read(), filename, token, first_row, input_col, target_col, rps_rate)
        return jsonify({}), 202, {"Location": url_for("tasks.task_status",
                                                      task_id=task.id)}
            # wb = payload(file, token, first_row, input_col, target_col, rps_rate)
        # except ValueError as e:
        #     current_app.logger.error(f"Value error on workbook indexing\n{e}")
        #     flash("Недопустимый индекс ячейки", "Ошибка сервера")
        #     return redirect(url_for("index"))
        #
        # except InvalidTokenError as e:
        #     current_app.logger.error(f"API Authentification error\n{e}")
        #     flash("Неверный токен", "Ошибка сервера")
        #     return redirect(url_for("index"))
        #
        # except WBReaderError as e:
        #     current_app.logger.error(f"File reader error\n{e}")
        #     flash("Ошибка обработки файла", "Ошибка сервера")
        #     return redirect(url_for("index"))
        #
        # except RequestException as e:
        #     current_app.logger.error(f"API request error\n{e}")
        #     flash("Ошбика запроса к VK API", "Ошибка сервера")
        #     return redirect(url_for("index"))
        #
        # except WBWriterError as e:
        #     current_app.logger.error(f"Writing to file error\n{e}")
        #     flash("Ошбика записи файла", "Ошибка сервера")
        #     return redirect(url_for("index"))
        #
        # else:
        # current_app.logger.info("Payload finished, sending file")
        # wb = result.get("result", )
        # virtual_workbook = BytesIO()
        # wb.save(virtual_workbook)
        # virtual_workbook.seek(0)
        #
        # return send_file(virtual_workbook, as_attachment=True, download_name=f"vkcc_{filename}",
        #                  mimetype="application/vnd.ms-excel")
    else:
        flash("Неверное расширение файла", "Ошибка")

        # return redirect(url_for("index"))
        return jsonify({'redirect': url_for('index')})


@bp.get("/status/<task_id>")
def task_status(task_id):
    task = tasks.payload.AsyncResult(task_id)
    if task.state == "PENDING":
        # job did not start yet
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending..."
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", "")
        }
        if "result" in task.info:
            # response["result"] = task.info["result"]
            response["redirect"] = url_for("tasks.get_result", task_id=task_id)
            # return redirect(url_for("get_result", task_id=task_id))
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    return jsonify(response)


@bp.get("/result/<task_id>")
def get_result(task_id):
    task = tasks.payload.AsyncResult(task_id)
    result = task.info["result"]
    filename = task.info["filename"]

    current_app.logger.info("Payload finished, sending file")
    # wb = result
    # virtual_workbook = BytesIO()
    # wb.save(virtual_workbook)
    # virtual_workbook.seek(0)

    return send_file(BytesIO(result), as_attachment=True, download_name=f"vkcc_{filename}",
                     mimetype="application/vnd.ms-excel")
