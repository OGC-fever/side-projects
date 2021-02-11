from flask import request
from mods.db_crud import post
from config import app


@app.route("/card_info", methods=["POST", "GET"])
def card_info():
    id = request.form['id']
    data = post.query.filter_by(id=id).first()
    data = {"id": data.id,
            "name": data.name,
            "msg": data.msg}
    return data
