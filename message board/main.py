from flask import app
from config import app
from mods.image_route import *
from mods.card import *
from mods.msg import *


# @app.route("/", methods=["GET"])
# @app.route("/msg", methods=["GET", "POST"])
# def messages():
#     code = verify()
#     if request.method == "GET":
#         data = post.query.order_by(post.id.desc()).all()
#         # data_count = db.session.query(post.id).count()
#         data_count = post.query.count()
#         if data_count == 0:
#             return render_template("message.html", data="", code=code)
#         else:
#             return render_template("message.html", data=data[:10], code=code)

#     name = request.form['name']
#     msg = request.form['msg']
#     file = request.files["upload"]
#     if name == "":
#         name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
#     if check_file(file.filename):  # file exist
#         image = sqlite3.Binary(make_timg(file, "image").getbuffer())
#         timg = sqlite3.Binary(make_timg(file, "timg").getbuffer())
#     else:  # file isn't exist
#         if msg == "":  # msg isn't exist
#             return ("", 204)
#         image = None
#         timg = None  # msg exist
#     data = post(name=name, msg=msg, image=image, timg=timg, code=code)
#     data.post()
#     return redirect(url_for("messages"))

# @ app.errorhandler(HTTPException)
# @ app.errorhandler(InternalServerError)
# @ app.errorhandler(TypeError)
# def not_found(e):
#     return render_template("oops.html")


if __name__ == "__main__":
    app.run(debug=True)
