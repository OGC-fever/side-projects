from flask import render_template, request, redirect, url_for
import sqlite3
import random

from msg.mods.form import check_file, dummy_msg, resize_img
from msg.mods.msg_db import post
from msg.config import app


@app.route("/", methods=["GET", "POST"])
@app.route("/msg", methods=["GET", "POST"])
# @app.route("/msg/<int:page>", methods=["GET"])
@app.route("/msg/more", methods=["GET", "POST"])
def msg(page=1):
    page_limit = 20
    if str(request.url_rule) in ("/msg", "/"):  # normal
        if request.method == "GET":
            try:
                data = post.query.order_by(post.time.desc()).limit(
                    page_limit).offset((page - 1) * page_limit)
            except:
                data = None
            if data:
                return render_template("msg.html", data=data)
            else:
                return render_template("msg.html")

        if request.method == "POST":  # new post
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

    if str(request.url_rule) == "/msg/more":  # ajax
        if request.method == "POST":
            page = int(request.form["page"])
            data = post.query.order_by(post.time.desc()).limit(
                page_limit).offset((page - 1) * page_limit)
        record = {"id": [], "name": [], "msg": []}
        for rec in data:
            record['id'].append(rec.id)
            record['name'].append(rec.name)
            record['msg'].append(rec.msg)
        data = {"id": record['id'],
                "name": record['name'],
                "msg": record['msg']}
        return data
