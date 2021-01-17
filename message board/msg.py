from flask import Flask, render_template, request, url_for, redirect, Response
import sqlite3
import random
from werkzeug.exceptions import HTTPException, InternalServerError
from io import BytesIO
from flask import app
from modules.addon import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///message.db'
db = SQLAlchemy(app)


class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    msg = db.Column(db.Text, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    timg = db.Column(db.LargeBinary, nullable=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/test")
def index():
    data = post.query.all()
    return data


@app.route("/<type>/<int:id>", methods=["GET"])
def image_route(id, type):
    data = post.query.filter_by(id=id).first()
    if type == "image":
        image = BytesIO(data.image)
    elif type == "timg":
        image = BytesIO(data.timg)
    else:
        return redirect("msg")
    return Response(image, mimetype='image/jpeg', direct_passthrough=True)


@app.route("/", methods=["GET"])
@app.route("/msg", methods=["GET", "POST"])
def messages():
    db.create_all()
    if request.method == "GET":
        try:
            data = post.query.order_by(post.id.desc()).all()
        except:
            return render_template("message.html", data="")
        return render_template("message.html", data=data)
    name = request.form['name']
    msg = request.form['msg']
    file = request.files["upload"]
    if name == "":
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    if check_file(file.filename):  # file exist
        image = sqlite3.Binary(make_timg(file, "image").getbuffer())
        timg = sqlite3.Binary(make_timg(file, "timg").getbuffer())
    else:  # file isn't exist
        if msg == "":  # msg isn't exist
            return render_template("message.html")
        image = None
        timg = None  # msg exist
    data = post(name=name, msg=msg, image=image, timg=timg)
    db.session.add(data)
    db.session.commit()
    return redirect("msg")

# @ app.errorhandler(HTTPException)
# @ app.errorhandler(InternalServerError)
# @ app.errorhandler(TypeError)
# def not_found(e):
#     return render_template("oops.html")


if __name__ == "__main__":
    app.run(debug=True)
