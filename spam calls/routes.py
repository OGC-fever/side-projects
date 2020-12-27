from flask import Flask, render_template, request, url_for, redirect
from db_crud import init_db
import sqlite3

app = Flask(__name__)
init_db()
database = 'spam_calls.db'


@app.route("/query")
def query():
    return render_template("query_calls.html")


@app.route("/add")
def add():
    return render_template("add_calls.html")


@app.route("/add_calls", methods=["POST"])
def add_calls():
    if request.method == 'POST':
        phone = request.form['phone']
        comments = request.form['comments']
        sql = f"insert into calls (phone, comments) values (?, ?)"
        try:
            con = sqlite3.connect(database)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(sql, (phone, comments))
            con.commit()
            con.close()
            msg = "Successfully"
            data = [phone, comments]
        except:
            con.rollback()
            return render_template("oops.html")
    return render_template("result.html", data=data, msg=msg, action='add')


@app.route("/query_calls", methods=["POST"])
def query_calls():
    if request.method == 'POST':
        phone = request.form['phone']
        sql = f"select * from calls where phone = ?"
        try:
            con = sqlite3.connect(database)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(sql, (phone,))
            data = cur.fetchall()
            con.close()
            msg = ""
            if data == []:
                msg = None
                return render_template("result.html", action='query', msg=msg)
        except:
            con.rollback()
            return render_template("oops.html")
    return render_template("result.html", data=data, action='query', msg=msg)


@app.errorhandler(404)
def not_found(e):
    return render_template("oops.html")


@app.route("/")
@app.route("/about")
def about():
    sql = f"select * from calls order by id desc limit 5"
    if request.method == 'GET':
        try:
            con = sqlite3.connect(database)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            con.close()
            msg = ""
            if data == []:
                msg = None
                return render_template("result.html", action='query', msg=msg)
        except:
            con.rollback()
            return render_template("oops.html")
    return render_template("index.html", data=data)


@app.route("/rank_up/<int:id>")
def rank_up(id):
    sql = f"update calls set rank = rank + 1 where id = ?"
    try:
        con = sqlite3.connect(database)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql, (id,))
        con.commit()
        cur.execute(f"select * from calls where id = '{id}'")
        data = cur.fetchall()
        con.close()
    except:
        con.rollback()
        return render_template("oops.html")
    return render_template("result.html", data=data, action='query')


@app.route("/rank_down/<int:id>")
def rank_down(id):
    sql = f"update calls set rank = rank - 1 where id = ?"
    try:
        con = sqlite3.connect(database)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(sql, (id,))
        con.commit()
        cur.execute(f"select * from calls where id = '{id}'")
        data = cur.fetchall()
        con.close()
    except:
        con.rollback()
        return render_template("oops.html")
    return render_template("result.html", data=data, action='query')


if __name__ == "__main__":
    app.run(debug=True)
