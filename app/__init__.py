from flask import Flask
from .extensions import db, migrate

from .config import Config
from .routes.wallet import wallet


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(wallet)

    db.init_app(app)
    migrate.init_app(app)

    with app.app_context():
        db.create_all()

    return app
