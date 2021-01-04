from flask import Flask, render_template, request, url_for, redirect
from init_db import init_db
import sqlite3
from werkzeug.exceptions import HTTPException, InternalServerError

app = Flask(__name__)
database = 'spam_calls.db'
init_db(database)


@app.route("/", methods=["GET"])
@app.route("/about", methods=["GET"])
def about():
    sql = "select * from calls order by id desc limit 5"
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql)
        data = cur.fetchall()
    if data == []:
        return render_template("about.html", action='query', msg="")
    return render_template("about.html", data=data)


@app.route("/msg", methods=["GET", "POST"])
def msg():
    if request.method == "GET":
        sql = "select * from msgs order by id desc limit 20"
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
    sql = "insert into msgs (name, msg) values (?, ?)"
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql, (name, msg))
        con.commit()
    return redirect(url_for("msg"))


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "GET":
        return render_template("add.html")
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


@app.route("/query", methods=["POST", "GET"])
def query():
    if request.method == "GET":
        return render_template("query.html")
    phone = request.form['phone']
    rank = request.form['rank']
    sql = "select * from calls where phone like ? order by time desc limit 10"
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if rank == "":
            cur.execute(sql, ('%' + phone + '%',))
        else:
            sql = sql.replace("?", "? and rank >= ?")
            cur.execute(sql, ('%' + phone + '%', rank,))
        data = cur.fetchall()
    if data == []:
        msg = "No record"
        return render_template("result.html", action='query', msg=msg)
    return render_template("result.html", data=data, action='query')


@app.errorhandler(HTTPException)
@app.errorhandler(InternalServerError)
def not_found(e):
    return render_template("oops.html")


@app.route("/rank_up/<int:id>", methods=["GET"])
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


@app.route("/rank_down/<int:id>", methods=["GET"])
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
