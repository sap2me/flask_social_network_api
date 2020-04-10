from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import TestConfig, ProdConfig

db = SQLAlchemy()

def create_app(config_class=TestConfig):
	app = Flask(__name__)
	app.config.from_object(config_class)
	db.init_app(app)

	from app.views import auth
	from app.api import api

	app.register_blueprint(auth)
	app.register_blueprint(api, url_prefix='/api')

	return app

def create_db():
	app = create_app()
	with app.app_context():
		db.create_all()