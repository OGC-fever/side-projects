from flask import render_template
from mods.db_crud import post
from config import app

@app.route("/post/<id>", methods=["GET", "POST"])
def card(id):
    data = post.query.filter_by(id=id).first()
    return render_template("card.html", data=data, id=id)
