from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)

	from app.views import auth
	from app.api import api

	app.register_blueprint(auth)
	app.register_blueprint(api, url_prefix='/api')

	return app