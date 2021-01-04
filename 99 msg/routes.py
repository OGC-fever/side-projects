from flask import Flask, render_template, request, url_for, redirect
from init_db import init_db
import sqlite3
import random
from werkzeug.exceptions import HTTPException, InternalServerError

app = Flask(__name__)
database = 'msg.db'
init_db(database)


@app.route("/", methods=["GET"])
@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/msg", methods=["GET", "POST"])
def msg():
    if request.method == "GET":
        sql = "select * from msgs order by id desc limit 99"
        with sqlite3.connect(database) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(sql)
            data = cur.fetchall()
        if data == []:
            return render_template("message.html", data="")
        return render_template("message.html", data=data)
    name = request.form['name']
    msg = request.form['msg']
    if name == "":
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    sql = "insert into msgs (name, msg) values (?, ?)"
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql, (name, msg))
        con.commit()
    return redirect(url_for("msg"))


@app.errorhandler(HTTPException)
@app.errorhandler(InternalServerError)
def not_found(e):
    return render_template("oops.html")


if __name__ == "__main__":
    app.run(debug=True)
