from flask import request, redirect, url_for
import random

from mods.form import dummy_msg
from mods.db_crud import reply
from config import app


@app.route("/reply", methods=["POST"])
def re():
    name = request.form['name']
    msg = request.form['msg']
    if name == "":
        name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
    if msg == "":  # msg isn't exist
        msg = dummy_msg()
    data = reply(name=name, msg=msg, ref_id=76)
    data.post()
    return redirect(url_for("msg"))
