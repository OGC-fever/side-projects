from flask import Flask, redirect, render_template, request, url_for
from db_crud import init_db, get_data
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


@app.route("/add_calls", methods=["GET", "POST"])
def add_calls():
    if request.method == 'POST':
        phone = request.form['phone']
        comments = request.form['comments']
        con = sqlite3.connect(database)
        cur = con.cursor()
        sql = f"insert into calls (phone,comments) values ('{phone}','{comments}')"
        try:
            cur.execute(sql)
            con.commit()
            con.close()
            msg = "Successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"
    else:
        msg = "Access Denial"
    return render_template("result.html", msg=msg)


@app.route("/query_calls")
def query_calls():
    con = sqlite3.connect(database)
    cur = con.cursor()
    phone = request.form['phone']
    sql=f"select * from calls where phone = '{phone}'"
    try:
        cur.execute(sql)
        con.commit()
        con.close()
        msg = "Successfully added"
    except:
        con.rollback()
        msg = "Error in insert operation"
    return render_template("result.html", msg=msg)


@app.route("/")
@app.route("/about")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
