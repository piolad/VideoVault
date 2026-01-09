from flask import Blueprint, jsonify,request
from pydantic import ValidationError
from sqlalchemy import delete, update

from .models import Video, VideoCreate, VideoOut
from .db import db

bp = Blueprint("main", __name__)

@bp.get("/")
def hello():
    return jsonify("Hello World!")

@bp.get("/ping")
def ping():
    return jsonify(ok=True)

# read
@bp.get("/video")
@bp.get("/videos")
@bp.get("/video/<int:id>")
def read_video(id=None):
    if id == None:
        videos = Video.query.order_by(Video.id.desc()).limit(50).all()
        return jsonify(  [ VideoOut.model_validate(v).model_dump()   for v in videos ])
    

    v = db.session.get(Video, id)
    if v is None:
        return jsonify(ok=False, reason="not found"), 404
    return jsonify(VideoOut.model_validate(v).model_dump())


# create
@bp.post("/video")
@bp.post("/video/<int:id>")
def create_new_video(id=None):
    json_data = request.get_json(silent=True) or {}
    
    if id is not None:
        json_data["id"] = id

    # Validation
    try:
        data = VideoCreate.model_validate(json_data)
    except ValidationError as e:
        return jsonify(ok=False, errors=e.errors()),400
    
    if id is not None:
        v  = db.session.get(Video, id)
        if v is not None:
            return jsonify(ok=False,errors={"msg":"Film of that id already exists"}),400

    v = Video(name=data.name, id=id)
    
    db.session.add(v)
    db.session.commit()
    

    return jsonify(ok=True), 201


# update
@bp.patch("/video/<int:id>")
def patch_video(id=None):
    json_data = request.get_json(silent=True) or {}

    if id is not None:
        json_data["id"] = id

    if id is None:
        return jsonify(ok=False, reason="id is None"), 404

    # to forbid injections
    try:
        data = VideoCreate.model_validate(json_data)
    except ValidationError as e:
        return jsonify(ok=False, errors=e.errors()),400
    
    stmt = update(Video).where(Video.id == id).values(data.model_dump())

    result = db.session.execute(stmt)
    db.session.commit()

    return jsonify(ok=True)

    

# delete
@bp.delete("/video/<int:id>")
def delete_video(id=None):
    if id is None:
        return jsonify(ok=False, reason="id is None"), 404

    stmt = delete(Video).where(Video.id == id)
    
    result = db.session.execute(stmt)
    db.session.commit()
    
    if result.rowcount == 0:
        return jsonify(ok=False, reason="not found"), 404
    
    return jsonify(ok=True)


