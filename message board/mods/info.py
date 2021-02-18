from flask import request, redirect, url_for
from mods.form import dummy_msg
import random
from mods.db_crud import post, reply
from config import app
from flask import render_template


@app.route("/info/<int:id>", methods=["GET"])
def info(id):
    data = post.query.filter_by(id=id).first()
    comment = reply.query.filter_by(
        ref_id=id).order_by(reply.time.desc()).all()
    return render_template("info.html", data=data, comment=comment, id=id)


@app.route("/reply/<int:id>", methods=["POST"])
def comment(id):
    name = request.form['name']
    msg = request.form['msg']
    if name == "":
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    if msg == "":  # msg isn't exist
        msg = dummy_msg()
    data = reply(name=name, msg=msg, ref_id=id)
    data.post()
    post.renew_time(id)
    return redirect(url_for("info", id=id))
