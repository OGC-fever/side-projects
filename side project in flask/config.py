from flask.app import Flask

msg_app = Flask(__name__, template_folder="msg/templates",
            static_folder="msg/static")
msg_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///msg/message.db'
msg_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
msg_app.config['JSON_AS_ASCII'] = False


scraper_app = Flask(
    __name__, template_folder="scraper/templates", static_folder="scraper/static")
scraper_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
scraper_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
scraper_app.config['JSON_AS_ASCII'] = False
