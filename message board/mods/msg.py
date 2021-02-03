from flask import render_template, request, redirect, url_for
import sqlite3
import random

from mods.form import check_file, dummy_msg, resize_img
from mods.db_crud import post
from config import app


@app.route("/", methods=["GET", "POST"])
@app.route("/msg", methods=["GET", "POST"])
def msg():
    if request.method == "GET":
        try:
            data = post.query.order_by(post.time.desc()).limit(60).all()
            return render_template("message.html", data=data)
        except:
            return render_template("message.html")
    name = request.form['name']
    msg = request.form['msg']
    file = request.files["upload"]
    if name == "":
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    if msg == "":  # msg isn't exist
        msg = dummy_msg()
    if check_file(file.filename):  # file exist
        def pack(type):
            return sqlite3.Binary(resize_img(file, type).getbuffer())
        image = pack("image")
        timg = pack("timg")
        data = post(name=name, msg=msg, image=image, timg=timg)
        data.post()
    return redirect(url_for("msg"))
