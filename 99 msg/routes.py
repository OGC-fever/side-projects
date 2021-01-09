from flask import Flask, render_template, request, url_for, redirect, send_file, Response
from flask.helpers import flash
import sqlite3
import random
from werkzeug.exceptions import HTTPException, InternalServerError
from io import BytesIO
from flask import app
from modules.addon import *

app = Flask(__name__)
database = 'msg.db'


@app.route("/<type>/<int:id>", methods=["GET"])
def image_route(id, type):
    sql = f"select {type} from msg where id = {id}"
    # sql = "select ? from msg where id = ?"
    data = db_crud(database=database, sql=sql, prm="",
                   fetch="one", commit=False, query=False)
    image = BytesIO(data[0])
    # return send_file(image, mimetype="image/png") # standard
    # for pythonanywhere
    return Response(image, mimetype='image/jpeg', direct_passthrough=True)


@app.route("/", methods=["GET"])
@app.route("/msg", methods=["GET", "POST"])
def msg():
    limit = 49
    init_db(database, 49)
    sql = {"read": f"select * from msg order by id desc limit {limit}",
           "create": "insert into msg (name, msg, image, thumbnail) values (?, ?, ?, ?)"}
    if request.method == "GET":
        data = db_crud(database=database,
                       sql=sql["read"], prm="", fetch="all", commit=False, query=False)
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
        name, msg, image, thumbnail), fetch="all", commit=True, query=False)
    return redirect(url_for("msg"))

# @ app.errorhandler(HTTPException)
# @ app.errorhandler(InternalServerError)
# @ app.errorhandler(TypeError)
# def not_found(e):
#     return render_template("oops.html")


if __name__ == "__main__":
    app.run(debug=True)
