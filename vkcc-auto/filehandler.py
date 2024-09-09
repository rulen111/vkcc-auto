from io import BytesIO

from flask import Blueprint, flash, redirect, render_template, request, send_file, current_app
from werkzeug.utils import secure_filename

from .src import payload

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
            flash("No file part")

            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")

            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            current_app.logger.info(f"Uploaded [{filename}]")

            try:
                wb = payload(file, current_app.config["TOKEN"])
            except OSError as e:
                current_app.logger.error(f"Error during payload execution\n{e}")
                flash(str(e))

                return redirect(request.url)
            else:
                current_app.logger.info("Payload finished, sending file")
                virtual_workbook = BytesIO()
                wb.save(virtual_workbook)
                virtual_workbook.seek(0)

                return send_file(virtual_workbook, as_attachment=True, download_name=f"vkcc_{filename}",
                                 mimetype="application/vnd.ms-excel")

    return render_template("index.html")
