from flask import Blueprint, jsonify,request
from sqlalchemy import text

from .db import db

bp = Blueprint("hc", __name__)

@bp.get("/health/live")
def live():
    return jsonify(ok=True)

@bp.get("/health/ready")
def ready():
    db.session.execute(text("SELECT 1"))
    return jsonify(ok=True)