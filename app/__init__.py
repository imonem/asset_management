from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from .config import Config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from . import routes

        app.register_blueprint(routes.bp)
        db.create_all()  # Create tables on first run

    return app
