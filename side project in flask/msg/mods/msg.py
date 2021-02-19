from flask import render_template, request, redirect, url_for
import sqlite3
import random

from msg.mods.form import check_file, dummy_msg, resize_img
from msg.mods.msg_db_crud import post
from msg.config import app


@app.route("/", methods=["GET", "POST"])
@app.route("/msg", methods=["GET", "POST"])
@app.route("/msg/<int:page>", methods=["GET", "POST"])
def msg(page=1):
    page_limit = 30
    if request.method == "GET":
        try:
            data = post.query.order_by(post.time.desc()).limit(
                page_limit).offset((page-1)*page_limit)
            return render_template("msg.html", data=data)
        except:
            return render_template("msg.html")
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
