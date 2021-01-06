from flask import Flask, render_template, request, url_for, redirect
from flask.helpers import flash
from init_db import init_db
import sqlite3
import random
from werkzeug.exceptions import HTTPException, InternalServerError
import base64
from io import BytesIO
from werkzeug.utils import secure_filename


app = Flask(__name__)

database = 'msg.db'
init_db(database)


# @app.route("/test", methods=["GET"])
# def test():
#     # img = plt.imread("static/pic/upload/test.png")
#     # buf = BytesIO()
#     # plt.imsave(buf, img, format="png")
#     # data = base64.b64encode(buf.getbuffer()).decode("ascii")

#     sql = "select image from msg order by id desc limit 1"
#     with sqlite3.connect(database) as con:
#         con.row_factory = sqlite3.Row
#         cur = con.cursor()
#         cur.execute(sql)
#         data = cur.fetchone()[0]
#     return f"<img src='data:image/png;base64,{data}'/>"


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


def check_file(filename, extensions):
    if "." in filename and filename.split(".")[-1].lower() in extensions:
        return True
    else:
        return False


@app.route("/", methods=["GET"])
@app.route("/msg", methods=["GET", "POST"])
def msg():
    sql = {"read": "select * from msg order by id desc limit 99",
           "create": "insert into msg (name, msg, image) values (?, ?, ?)"}
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
    if not name:
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    msg = request.form['msg']
    file = request.files["upload"]
    extensions = {'jpg', 'jpeg', "png", "gif"}
    if file.filename and check_file(file.filename, extensions):
        buf = BytesIO()
        file.save(buf)
        image = base64.b64encode(buf.getbuffer())
    else:
        image = None
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql["create"], (name, msg, image))
        con.commit()
    return redirect(url_for("msg"))


@app.errorhandler(HTTPException)
@app.errorhandler(InternalServerError)
def not_found(e):
    return render_template("oops.html")


if __name__ == "__main__":
    app.run(debug=True)
