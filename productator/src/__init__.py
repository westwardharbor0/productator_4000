from flask import Flask
from os import environ
from flask_sqlalchemy import SQLAlchemy

from .offers_client import OffersClient
from .messages import GeneralMessages
from .utils import generate_db_connection_string, generate_config_dict


db = SQLAlchemy()


def make_app() -> Flask:
    """
    Creates app and setups all needed stuff
    :return: complete Flask app
    """
    app = Flask(__name__)
    app.logger.info(GeneralMessages.starting_api)

    setup_configuration(app)
    setup_database_access(app)
    setup_endpoints(app)
    setup_offers_service(app)

    return app


def setup_configuration(app: Flask):
    """
    Loads the configuration file and stores in the app object
    :param app: Flask app
    """
    config_path = environ.get("PRODUCTATOR_CONFIG")
    if not config_path:
        raise Exception("PRODUCTATOR_CONFIG path is not set in env vars")

    app.config["config_file"] = generate_config_dict(config_path)
    app.logger.info(GeneralMessages.initialized_config)


def setup_offers_service(app: Flask):
    """
    Prepares the offers client
    :param app: Flask app
    """
    app.config["offers_service"] = OffersClient(
        base=(
            # offers service address can be changed using ENV var
            environ.get("OFFERS_MS_ADDRESS") or app.config["config_file"]["offers_address"]
        ),
        token=app.config["config_file"].get("offers_token")
    )
    app.logger.info(GeneralMessages.initialized_offers)


def setup_database_access(app: Flask):
    """
    Creates a cursor to access DB
    :param app: Flask app
    """
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = generate_db_connection_string(
        app.config["config_file"]
    )
    db.init_app(app)
    app.logger.info(GeneralMessages.initialized_db)


def setup_endpoints(app: Flask):
    """
    Loads and assign all the endpoints to app
    :param app: Flask app
    """
    with app.app_context():
        from .endpoints import offer
        from .endpoints import product

    app.logger.info(GeneralMessages.initialized_routes)
