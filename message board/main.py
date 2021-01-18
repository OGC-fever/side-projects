from flask import Flask
from flask import app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///message.db'
db = SQLAlchemy(app)

from mods.routes import *

if __name__ == "__main__":
    app.run(debug=True)
