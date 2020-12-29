from flask import Flask, render_template, request
from db_crud import init_db
from mods.about import about
import sqlite3
from werkzeug.exceptions import HTTPException, InternalServerError

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
    # if request.method == 'POST':
    phone = request.form['phone']
    comments = request.form['comments']
    sql = "insert into calls (phone, comments) values (?, ?)"
    # try:
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql, (phone, comments))
    con.commit()
    con.close()
    msg = "Successfully"
    data = {"phone": phone, "comments": comments}
    # except:
    #     con.rollback()
    #     return render_template("oops.html")
    return render_template("result.html", data=data, msg=msg, action='add')


@app.route("/query_calls", methods=["POST"])
def query_calls():
    # if request.method == 'POST':
    phone = request.form['phone']
    sql = "select * from calls where phone like ? order by time desc"
    # try:
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql, ('%'+phone+'%',))
    data = cur.fetchall()
    con.close()
    msg = ""
    if data == []:
        msg = None
        return render_template("result.html", action='query', msg=msg)
        # except:
        #     con.rollback()
        #     return render_template("oops.html")
    return render_template("result.html", data=data, action='query', msg=msg)


@app.errorhandler(HTTPException)
@app.errorhandler(InternalServerError)
def not_found(e):
    return render_template("oops.html")


@app.route("/", methods=["POST", "GET"])
@app.route("/about", methods=["POST", "GET"])
def index():
    return about(database)


@app.route("/rank_up/<int:id>", methods=["POST", "GET"])
def rank_up(id):
    sql = "update calls set rank = rank + 1 where id = ?"
    # try:
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql, (id,))
    con.commit()
    sql = "select * from calls where id = ?"
    cur.execute(sql, (id,))
    data = cur.fetchall()
    con.close()
    # except:
    #     con.rollback()
    #     return render_template("oops.html")
    return render_template("result.html", data=data, action='query')


@app.route("/rank_down/<int:id>", methods=["POST", "GET"])
def rank_down(id):
    sql = "update calls set rank = rank - 1 where id = ?"
    # try:
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(sql, (id,))
    con.commit()
    sql = "select * from calls where id = ?"
    cur.execute(sql, (id,))
    data = cur.fetchall()
    con.close()
    # except:
    #     con.rollback()
    #     return render_template("oops.html")
    return render_template("result.html", data=data, action='query')


if __name__ == "__main__":
    app.run(debug=True)
