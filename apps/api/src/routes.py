from flask import Blueprint, jsonify
from .models import Video


bp = Blueprint("main", __name__)

@bp.get("/")
def hello():
    return jsonify("Hello World!")

@bp.get("/ping")
def ping():
    return jsonify(ok=True)


@bp.get("/videos")
def list_video_ids():
    videos = Video.query.order_by(Video.id.desc()).limit(50).all()
    return jsonify(  [ {"id": v.id}    for v in videos ])
