import os
from flask import Flask, render_template
from celery import Celery, Task

from . import views, config


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app(test_config=None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load default config
        app.config.from_object(config.DefaultConfig)
        # try to load config with sensitive data using path from envvar
        try:
            app.config.from_envvar("VKCCAUTO_SETTINGS")
        except Exception:
            app.logger.warning("Path to secret config file not found in env. "
                               "Make sure you pass VK API access token to this app config dict")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    celery_init_app(app)

    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    # register core logic blueprint
    app.register_blueprint(views.bp)

    return app
