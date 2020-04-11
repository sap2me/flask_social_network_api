import json

from random_text import get_random_text
from tools import get_random_login, generate_password


class BotFactory:

	def __init__(self):
		self._load_settings()

	def _load_settings(self):
		with open('config.json') as file:
			self.settings = json.load(file)

	