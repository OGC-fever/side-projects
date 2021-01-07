from flask import Flask, render_template, request, url_for, redirect, send_file
from flask.helpers import flash
from PIL import Image
from init_db import init_db
import sqlite3
import random
from werkzeug.exceptions import HTTPException, InternalServerError
import base64
from io import BytesIO


app = Flask(__name__)

database = 'msg.db'
init_db(database)


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


def check_file(filename, file_exts):
    if "." in filename and filename.split(".")[-1].lower() in file_exts:
        return True
    else:
        return False


def get_file_ext(filename):
    ext = filename.split(".")[-1].upper()
    if ext == "JPG":
        ext = "JPEG"
    return ext


@app.route("/image/<int:id>", methods=["GET", "POST"])
def image_route(id):
    sql = "select image from msg where id = ?"
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql, (id,))
        result = cur.fetchone()
        image = BytesIO(result[0])
    return send_file(image, mimetype="image/png")


@app.route("/", methods=["GET"])
@app.route("/msg", methods=["GET", "POST"])
def msg():
    sql = {"read": "select * from msg order by id desc limit 99",
           "create": "insert into msg (name, msg, image, thumbnail) values (?, ?, ?, ?)"}
    if request.method == "GET":
        with sqlite3.connect(database) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(sql["read"])
            data = cur.fetchall()
        if data == []:
            return render_template("message.html", data="")
        return render_template("message.html", data=data)
    name = request.form['name']
    msg = request.form['msg']
    file = request.files["upload"]
    file_exts = {'jpg', 'jpeg', "png", "gif"}
    thumbnail_size = (500, 500)
    image, thumbnail = None, None
    if not name:
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    if not msg and not check_file(file.filename, file_exts):
        return redirect(url_for("msg"))
    if file.filename and check_file(file.filename, file_exts):
        buf_file = BytesIO()
        buf_thumb = BytesIO()
        file.save(buf_file)
        image = sqlite3.Binary(buf_file.getbuffer())
        im = Image.open(file)
        im.thumbnail(thumbnail_size)
        im.save(buf_thumb, get_file_ext(file.filename))
        thumbnail = base64.b64encode(buf_thumb.getbuffer()).decode()
    else:
        return redirect(url_for("msg"))    
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql["create"], (name, msg, image, thumbnail))
        con.commit()
    return redirect(url_for("msg"))


# @ app.errorhandler(HTTPException)
# @ app.errorhandler(InternalServerError)
# @ app.errorhandler(TypeError)
# def not_found(e):
#     return render_template("oops.html")


if __name__ == "__main__":
    app.run(debug=True)
