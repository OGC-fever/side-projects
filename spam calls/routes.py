from flask import Flask, render_template, request
from mods.init_db import init_db
import sqlite3
from werkzeug.exceptions import HTTPException, InternalServerError

app = Flask(__name__)
database = 'spam_calls.db'
init_db(database)


@app.route("/query")
def query():
    return render_template("query_calls.html")


@app.route("/add")
def add():
    return render_template("add_calls.html")


@app.route("/add_calls", methods=["POST"])
def add_calls():
    phone = request.form['phone']
    comments = request.form['comments']
    sql = "insert into calls (phone, comments) values (?, ?)"
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql, (phone, comments))
        con.commit()
    msg = "Successfully"
    data = {"phone": phone, "comments": comments}
    return render_template("result.html", data=data, msg=msg, action='add')


@app.route("/query_calls", methods=["POST"])
def query_calls():
    phone = request.form['phone']
    rank = request.form['rank']
    # return phone
    if rank == "":
        sql = "select * from calls where phone like ? order by time desc"
    else:
        sql = "select * from calls where phone like ? and rank >= ? order by time desc"
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if rank == "":
            cur.execute(sql, ('%'+phone+'%',))
        else:
            cur.execute(sql, ('%'+phone+'%', rank))
        data = cur.fetchall()
    msg = ""
    if data == []:
        msg = None
        return render_template("result.html", action='query', msg=msg)
    return render_template("result.html", data=data, action='query', msg=msg)


@app.errorhandler(HTTPException)
@app.errorhandler(InternalServerError)
def not_found(e):
    return render_template("oops.html")


@app.route("/", methods=["POST", "GET"])
@app.route("/about", methods=["POST", "GET"])
def about():
    sql = "select * from calls order by id desc limit 5"
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql)
        data = cur.fetchall()
    msg = ""
    if data == []:
        msg = None
        return render_template("result.html", action='query', msg=msg)
    return render_template("about.html", data=data)


@app.route("/rank_up/<int:id>", methods=["POST", "GET"])
def rank_up(id):
    sql = {"update": "update calls set rank = rank + 1 where id = ?",
           "read": "select * from calls where id = ?"}
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql["update"], (id,))
        con.commit()
        cur.execute(sql["read"], (id,))
        data = cur.fetchall()
    return render_template("result.html", data=data, action='query')


@app.route("/rank_down/<int:id>", methods=["POST", "GET"])
def rank_down(id):
    sql = {"update": "update calls set rank = rank - 1 where id = ?",
           "read": "select * from calls where id = ?"}
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql["update"], (id,))
        con.commit()
        cur.execute(sql["read"], (id,))
        data = cur.fetchall()
    return render_template("result.html", data=data, action='query')


if __name__ == "__main__":
    app.run(debug=True)
    # app.run()
