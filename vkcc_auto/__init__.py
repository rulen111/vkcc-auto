import os
from flask import Flask

from . import filehandler, config


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load default config
        app.config.from_object(config.DefaultConfig)
        # try to load config with sensitive data using path from envvar
        try:
            app.config.from_envvar("VKCCAUTO_SETTINGS")
        except Exception:
            app.logger.warning("Path to secret config file not found in env. "
                               "Make sure you pass VK API access token to this app config dict")
            pass
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register core logic blueprint
    app.register_blueprint(filehandler.bp)

    return app
