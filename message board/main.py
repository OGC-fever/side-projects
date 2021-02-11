from flask import app
from config import app
from mods.image_route import *
from mods.msg import *
from mods.db_crud import db
from mods.info import *

db.init_app(app)
db.create_all()

# @ app.errorhandler(HTTPException)
# @ app.errorhandler(InternalServerError)
# @ app.errorhandler(TypeError)
# def not_found(e):
#     return render_template("oops.html")


if __name__ == "__main__":
    app.run(debug=True)
