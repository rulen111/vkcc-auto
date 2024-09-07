import os
from io import BytesIO
from tempfile import NamedTemporaryFile

from flask import Flask, render_template, request, flash, redirect, send_file
from werkzeug.utils import secure_filename

from . import vkclient, wbhandler


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

    from . import filehandler
    app.register_blueprint(filehandler.bp)

    return app
