class TestConfig:
	SECRET_KEY = "3b2518fc775bfac95246a77c"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
	DEBUG = True

class ProdConfig:
	SECRET_KEY = "3b2518fc775bfac95246a77c"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
	DEBUG = False