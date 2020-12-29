from flask import render_template
import sqlite3

def about(database):
    sql = "select * from calls order by id desc limit 5"
    # if request.method == 'GET':
    # try:
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
    # except:
    #     con.rollback()
    #     return render_template("oops.html")
    return render_template("about.html", data=data)
