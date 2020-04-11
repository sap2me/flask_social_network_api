from waitress import serve

from app import create_app
from config import ProdConfig


if __name__ == '__main__':
	app = create_app(config_class=ProdConfig)
	serve(app, host='0.0.0.0', port=80)