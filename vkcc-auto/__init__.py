import os
from io import BytesIO
from tempfile import NamedTemporaryFile

from flask import Flask, render_template, request, flash, redirect, send_file
from werkzeug.utils import secure_filename

from . import vkclient, wbhandler




class Payload(object):
    """"""

    def __init__(self, input_file, client_token, first_row=2, input_col=1, target_col=2):
        self.client = vkclient.VKclient(client_token)
        self.wb = wbhandler.WBHandler(input_file)

        self.input_col = input_col
        self.target_col = target_col
        self.first_row = first_row

    def run(self):
        for row in range(self.first_row, self.wb.max_row + 1):
            link = self.wb.get_link(row, self.input_col)
            short_link = self.client.get_short_link(link)
            self.wb.write_new_link(row, self.target_col, short_link)

        return self.wb


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            file = request.files['file']
            fname = secure_filename(file.filename)
            # flash(f"Uploaded {fname}")
            # return redirect(request.url)
            pl = Payload(file, TOKEN)
            wb = pl.run()
            with NamedTemporaryFile() as tmp:
                wb.save(tmp.name)
                tmp.seek(0)
                return send_file(BytesIO(tmp.read()), as_attachment=True, download_name=f"{fname}_output.xlsx", mimetype="application/vnd.ms-excel")
        return render_template("index.html")

    return app
