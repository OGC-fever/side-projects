from flask import render_template, request, redirect, url_for
import sqlite3
import random

from mods.image_process import check_file, resize_img, verify
from mods.db_crud import post
from config import app


@app.route("/", methods=["GET", "POST"])
@app.route("/msg", methods=["GET", "POST"])
def msg():
    code = verify()
    if request.method == "GET":
        data = post.query.order_by(post.id.desc()).limit(15).all()
        data_count = post.query.count()
        if data_count == 0:
            return render_template("message.html", data="", code=code)
        else:
            return render_template("message.html", data=data, code=code)

    name = request.form['name']
    msg = request.form['msg']
    file = request.files["upload"]
    if name == "":
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    if msg == "":  # msg isn't exist
        return ("", 204)
    if check_file(file.filename):  # file exist
        def pack(type):
            return sqlite3.Binary(resize_img(file, type).getbuffer())
        image = pack("image")
        timg = pack("timg")
        data = post(name=name, msg=msg, image=image, timg=timg, code=code)
        data.post()
    return redirect(url_for("msg"))