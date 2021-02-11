from mods.db_crud import post
from config import app
from flask import render_template


@app.route("/info/<int:id>", methods=["POST", "GET"])
def info(id):
    data = post.query.filter_by(id=id).first()
    return render_template("info.html", data=data)
