from flask import Flask
from app.configs import env_configs, database, migration
from app import views


def create_app() -> Flask:
    app = Flask(__name__)

    env_configs.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    views.init_app(app)

    return app
