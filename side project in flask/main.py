from flask import app
from msg.config import app
from msg.mods.image_route import *
from msg.mods.msg import *
from msg.mods.msg_db import msg_db
from msg.mods.info import *

msg_db.init_app(app)
msg_db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
