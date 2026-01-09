from flask import Blueprint, jsonify,request

from .models import Video
from .db import db

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


# create
@bp.post("/video")
@bp.post("/video/<id>")
def create_new_video(id=None):
    json_data = request.get_json(silent=True) or {}

    name = json_data.get('name')
    
    if id is None:
        id = json_data.get('id')
    if id is not None:
        v  = Video.query.where(Video.id == id)
        # if v not null - fail
        pass 

    # Validation

    v = Video(name=name)
    
    db.session.add(v)
    db.session.commit()
    
    
    print(f"id is : {id}")

    return jsonify(ok=True)
