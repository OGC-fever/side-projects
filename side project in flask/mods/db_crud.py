from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import app
from config import app

db = SQLAlchemy(app)


class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True, index=True)
    msg = db.Column(db.Text, nullable=True, index=True)
    image = db.Column(db.LargeBinary, nullable=True)
    timg = db.Column(db.LargeBinary, nullable=True)
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def post(self):
        db.session.add(self)
        db.session.commit()

    def renew_time(id):
        data = post.query.filter_by(id=id).first()
        data.time = datetime.utcnow()
        db.session.commit()


class reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True, index=True)
    msg = db.Column(db.Text, nullable=True, index=True)
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ref_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    def post(self):
        db.session.add(self)
        db.session.commit()
