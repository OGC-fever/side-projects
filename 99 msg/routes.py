from flask import Flask, render_template, request, url_for, redirect, send_file, Response
from flask.helpers import flash
from PIL import Image
from init_db import init_db
import sqlite3
import random
from werkzeug.exceptions import HTTPException, InternalServerError
from io import BytesIO


app = Flask(__name__)

database = 'msg.db'
init_db(database)


def check_file(filename):
    file_exts = {'jpg', 'jpeg', "jfif", "png", "gif"}
    if filename and "." in filename and filename.split(".")[-1].lower() in file_exts:
        return True
    else:
        return False


def get_file_ext(filename):
    ext = filename.split(".")[-1].upper()
    if ext == "JPG":
        ext = "JPEG"
    return ext


def db_crud(database, sql, prm, fetchall, commit):
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if prm == "":
            cur.execute(sql)
        else:
            cur.execute(sql, prm)
        if fetchall:
            data = cur.fetchall()
        else:
            data = cur.fetchone()
        if commit:
            con.commit()
        else:
            return data


@app.route("/<kind>/<int:id>", methods=["GET", "POST"])
def image_route(id, kind):
    sql = f"select {kind} from msg where id = {id}"
    # sql = "select ? from msg where id = ?"
    data = db_crud(database=database, sql=sql, prm="",
                   fetchall=False, commit=False)
    image = BytesIO(data[0])
    # return send_file(image, mimetype="image/png")
    # for pythonanywhere
    return Response(image, mimetype='image/jpeg', direct_passthrough=True)


@app.route("/", methods=["GET"])
@app.route("/msg", methods=["GET", "POST"])
def msg():
    sql = {"read": "select * from msg order by id desc limit 99",
           "create": "insert into msg (name, msg, image, thumbnail) values (?, ?, ?, ?)"}
    if request.method == "GET":
        data = db_crud(database=database,
                       sql=sql["read"], prm="", fetchall=True, commit=False)
        if data == []:
            return render_template("message.html", data="")
        return render_template("message.html", data=data)
    name = request.form['name']
    msg = request.form['msg']
    file = request.files["upload"]
    if not name:
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    if check_file(file.filename):
        image_size, thumbnail_size = (1000, 1000), (300, 300)
        buf_file, buf_thumb = BytesIO(), BytesIO()
        # file.save(buf_file) #just save
        im_image = Image.open(file)
        im_image.thumbnail(image_size)
        im_image.save(buf_file, get_file_ext(file.filename))
        image = sqlite3.Binary(buf_file.getbuffer())

        im_thumb = Image.open(file)
        im_thumb.thumbnail(thumbnail_size)
        im_thumb.save(buf_thumb, get_file_ext(file.filename))
        # thumbnail = base64.b64encode(buf_thumb.getbuffer()).decode() #base64
        thumbnail = sqlite3.Binary(buf_thumb.getbuffer())
    else:
        if msg:
            image, thumbnail = None, None
        else:
            return redirect(url_for("msg"))
    db_crud(database=database, sql=sql["create"], prm=(
        name, msg, image, thumbnail), fetchall=True, commit=True)
    return redirect(url_for("msg"))


# @ app.errorhandler(HTTPException)
# @ app.errorhandler(InternalServerError)
# @ app.errorhandler(TypeError)
# def not_found(e):
#     return render_template("oops.html")


if __name__ == "__main__":
    app.run(debug=True)
