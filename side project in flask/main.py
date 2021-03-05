from flask import Flask, url_for
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound

from config import msg_app, ptt_app

from apps.msg.image_route import *
from apps.msg.info import *
from apps.msg.msg_db import msg_db
from apps.msg.msg import *

from apps.ptt.ptt import *

msg_db.init_app(msg_app)
msg_db.create_all()

app = Flask(__name__)
about = Flask(__name__)


@about.route("/", methods=["GET", "POST"])
def test():
    return render_template("about/about.html")


app.wsgi_app = DispatcherMiddleware(about, {
    "/msg": msg_app,
    '/ptt': ptt_app
})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
