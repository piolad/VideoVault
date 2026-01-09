from flask import Blueprint, jsonify
bp = Blueprint("main", __name__)

@bp.get("/")
def hello():
    return jsonify("Hello World!")

@bp.get("/ping")
def ping():
    return jsonify(ok=True)

