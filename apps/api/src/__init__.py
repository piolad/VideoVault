from flask import Flask
from time import sleep
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import logging

from .db import db
from .config import config
from .routes import bp as main_bp
from .hc import bp as healthchecks_bp


def create_app():
    app = Flask(__name__)

    gunicorn_logger = logging.getLogger("gunicorn.error")
    if gunicorn_logger.handlers:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        app.logger.propagate = False


    app.config["SQLALCHEMY_DATABASE_URI"] = config["database_url"]

    db.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(healthchecks_bp)

    with app.app_context():
        wait_for_db(app, attempts=8, delay=2.0)

    return app


def wait_for_db(app, attempts=8, delay=2.0):

    for i in range(1, attempts+1):
        try:
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        
        except OperationalError as e:
            if i == attempts:
                raise RuntimeError("Database connection failed after retries") from e

            app.logger.warning(
                "DB not reachable (attempt %s/%s). Retrying in %ss... Error: %s",
                i, attempts, delay, e)
            sleep(delay)

