from flask.app import Flask

msg_app = Flask(__name__)
msg_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apps/msg/message.db'
msg_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
msg_app.config['JSON_AS_ASCII'] = False


ptt_app = Flask(__name__)
ptt_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
ptt_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ptt_app.config['JSON_AS_ASCII'] = False
