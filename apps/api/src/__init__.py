from flask import Flask

from .db import db
from .config import config
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config["database_url"]

    db.init_app(app)
    app.register_blueprint(main_bp) 

    return app