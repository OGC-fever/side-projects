from flask import app
from msg.config import app
from msg.mods.image_route import *
from msg.mods.msg import *
from msg.mods.db_crud import db
from msg.mods.info import *

db.init_app(app)
db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
