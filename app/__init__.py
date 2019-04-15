import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import CONFIG

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(CONFIG[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disabling sqlalchemy event system

    CONFIG[config_name].init_app(app)

    root = CONFIG[config_name].APPLICATION_ROOT

    # flask migrate doesn't recognize the tables without this import
    from app.models import Application, Genre, ApplicationType, Session, Questionnaire

    # Set up extensions
    db.init_app(app)

    # Create app blueprints
    from app.routes.v1 import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix=root + '/')

    from app.routes.v1 import application as application_blueprint
    app.register_blueprint(application_blueprint, url_prefix=root + '/application')

    from app.routes.v1 import session as session_blueprint
    app.register_blueprint(session_blueprint, url_prefix=root + '/session')

    from app.routes.v1 import questionnaire as questionnaire_blueprint
    app.register_blueprint(questionnaire_blueprint, url_prefix=root + '/questionnaire')

    return app
