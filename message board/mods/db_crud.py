from datetime import datetime
from main import db


class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    msg = db.Column(db.Text, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    timg = db.Column(db.LargeBinary, nullable=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    code = db.Column(db.Text, nullable=True)

    def post(self):
        db.session.add(self)
        db.session.commit()
