from flask import Flask, render_template, request, url_for, redirect, send_file, Response
from flask.helpers import flash
from PIL import Image
import sqlite3
import random
from werkzeug.exceptions import HTTPException, InternalServerError
from io import BytesIO

app = Flask(__name__)


def init_db(database):
    sql = {
        "init_msg": "create table if not exists msg (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,msg TEXT NOT NULL,time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,image blob,thumbnail blob)"}
    db_crud(database=database, sql=sql["init_msg"],
            prm="", fetch=False, commit=True)


def check_file(filename):
    file_exts = {'jpg', 'jpeg', "jfif", "png", "gif"}
    if filename and "." in filename:
        if filename.split(".")[-1].lower() in file_exts:
            return True
    else:
        return False


def get_file_ext(filename):
    ext = filename.split(".")[-1].upper()
    if ext == "JPG":
        ext = "JPEG"
    return ext


def db_crud(database, sql, prm, fetch, commit):
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if prm == "":
            cur.execute(sql)
        if prm != "":
            cur.execute(sql, prm)
        if fetch != False:
            if fetch == "all":
                return cur.fetchall()
            if fetch == "one":
                return cur.fetchone()
        if commit:
            con.commit()


def make_timg(file, type):  # make thumbnail
    image_size = [(1000, 1000), (300, 300)]
    buf = BytesIO()
    im = Image.open(file)
    if type == "image":
        im.thumbnail(image_size[0])
    if type == "timg":
        im.thumbnail(image_size[1])
    im.save(buf, get_file_ext(file.filename))
    return buf


@app.route("/<type>/<int:id>", methods=["GET"])
def image_route(id, type):
    sql = f"select {type} from msg where id = {id}"
    # sql = "select ? from msg where id = ?"
    data = db_crud(database=database, sql=sql, prm="",
                   fetch="one", commit=False)
    image = BytesIO(data[0])
    # return send_file(image, mimetype="image/png") # standard
    # for pythonanywhere
    return Response(image, mimetype='image/jpeg', direct_passthrough=True)


@app.route("/", methods=["GET"])
@app.route("/msg", methods=["GET", "POST"])
def msg():
    sql = {"read": "select * from msg order by id desc limit 49",
           "create": "insert into msg (name, msg, image, thumbnail) values (?, ?, ?, ?)"}
    if request.method == "GET":
        data = db_crud(database=database,
                       sql=sql["read"], prm="", fetch="all", commit=False)
        if data == []:
            return render_template("message.html", data="")
        return render_template("message.html", data=data)
    name = request.form['name']
    msg = request.form['msg']
    file = request.files["upload"]
    if not name:
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    if check_file(file.filename):
        # file.save(buf_file) # just save
        # thumbnail = base64.b64encode(buf.getbuffer()).decode() # base64
        image = sqlite3.Binary(make_timg(file, "image").getbuffer())
        thumbnail = sqlite3.Binary(make_timg(file, "timg").getbuffer())
    else:
        if msg:
            image, thumbnail = None, None
        else:
            return redirect(url_for("msg"))
    db_crud(database=database, sql=sql["create"], prm=(
        name, msg, image, thumbnail), fetch="all", commit=True)
    return redirect(url_for("msg"))

# @ app.errorhandler(HTTPException)
# @ app.errorhandler(InternalServerError)
# @ app.errorhandler(TypeError)
# def not_found(e):
#     return render_template("oops.html")


database = 'msg.db'

if __name__ == "__main__":
    app.run(debug=True)
    init_db(database)
