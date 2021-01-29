from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import app
from config import app

db = SQLAlchemy(app)
db.init_app(app)


class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True, index=True)
    msg = db.Column(db.Text, nullable=True, index=True)
    image = db.Column(db.LargeBinary, nullable=True)
    timg = db.Column(db.LargeBinary, nullable=True)
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    code = db.Column(db.Text, nullable=True)

    def post(self):
        db.session.add(self)
        db.session.commit()
