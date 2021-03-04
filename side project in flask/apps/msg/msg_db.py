from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from config import msg_app

msg_db = SQLAlchemy(msg_app)


class post(msg_db.Model):
    id = msg_db.Column(msg_db.Integer, primary_key=True)
    name = msg_db.Column(msg_db.Text, nullable=True, index=True)
    msg = msg_db.Column(msg_db.Text, nullable=True, index=True)
    image = msg_db.Column(msg_db.LargeBinary, nullable=True)
    timg = msg_db.Column(msg_db.LargeBinary, nullable=True)
    time = msg_db.Column(msg_db.DateTime, default=datetime.utcnow, index=True)

    def post(self):
        msg_db.session.add(self)
        msg_db.session.commit()

    def renew_time(id):
        data = post.query.filter_by(id=id).first()
        data.time = datetime.utcnow()
        msg_db.session.commit()


class reply(msg_db.Model):
    id = msg_db.Column(msg_db.Integer, primary_key=True)
    name = msg_db.Column(msg_db.Text, nullable=True, index=True)
    msg = msg_db.Column(msg_db.Text, nullable=True, index=True)
    time = msg_db.Column(msg_db.DateTime, default=datetime.utcnow, index=True)
    ref_id = msg_db.Column(msg_db.Integer, msg_db.ForeignKey("post.id"))

    def post(self):
        msg_db.session.add(self)
        msg_db.session.commit()
