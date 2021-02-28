from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound

from config import msg_app, scraper_app

from msg.mods.image_route import *
from msg.mods.info import *
from msg.mods.msg_db import msg_db
from msg.mods.msg import *

from scraper.mods.test import *

msg_db.init_app(msg_app)
msg_db.create_all()

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(NotFound(), {
    # "/": msg_app,
    "/msg": msg_app,
    '/ptt': scraper_app
})


if __name__ == "__main__":
    app.run(debug=True)
    # print(app.mounts.keys())
    # run_simple('localhost', 5000, app, use_reloader=True,
            #    use_debugger=True, use_evalex=True)
