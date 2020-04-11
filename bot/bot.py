import requests
import json

from threading import Thread
from time import sleep
from random import randint, sample

from random_text import get_random_text
from exceptions import ApiError, LoginRequired
from tools import get_random_login, generate_password
from tools import headers as simple_headers
from models import URLS


def login_required(func):
	def wrapper(self, *args, **kwargs):
		if not self.jwt:
			raise LoginRequired('First do login before calling this function')
		func(self, *args, **kwargs)
	return wrapper

class Bot:

	def __init__(self, name=None, password=None, proxy=None):
		if not name:
			name = get_random_login()
		if not password:
			password = generate_password()
		self.jwt = None
		self.name = name
		self.password = password
		self.session = requests.Session()
		self.session.headers = simple_headers
		if proxy:
			self.proxy = proxy
			self.session.proxy = {
				"http": "http://" + proxy,
				"https": "https://" + proxy
			}

	def get_info(self):
		info = {
			"name": self.name,
			"password": self.password
		}
		return info

	def create_account(self):
		data = {
			"name": self.name,
			"password": self.password
		}
		try:
			response = self.session_post(URLS.SINGUP, data=data)
			res_data = response.json()
			print(res_data['message'])

		except Exception as e:
			print(f"Error with creating new account: {e}")

	def do_login(self):
		data = {
			"name": self.name,
			"password": self.password
		}
		try:
			response = self.session_post(URLS.LOGIN, data=data)
			res_data = response.json()
			self.jwt = res_data['jwt']
			print('Login success!')

		except Exception as e:
			print(f"Error with logging to account: {e}")

	@login_required
	def create_post(self, text=None):
		if not text:
			text = get_random_text()
		data = {
			"text": text
		}
		try:
			response = self.session_post(URLS.CREATE_POST, data=data, auth=True)
			res_data = response.json()
			print(res_data['message'])

		except Exception as e:
			print(f"Error with creating post: {e}")

	@login_required
	def like_post(self, post_id):
		data = {
			"post_id": int(post_id)
		}
		try:
			response = self.session_post(URLS.POST_LIKE, data=data, auth=True)
			res_data = response.json()
			
			print(res_data['message'])

		except Exception as e:
			print(f"Error with post like: {e}")

	def get_all_posts(self):
		response = self.session_get(URLS.GET_POSTS)
		res_json = response.json()
		return res_json

	def session_get(self, url, params={}, headers={}, cookies={}, timeout=(10, 10)):
		response = self.session.get(url, params=params, headers=headers,
									cookies=cookies, timeout=timeout)
		data = response.json()
		return response

	def session_post(self, url, params={}, data={}, headers={}, cookies={},
					 timeout=(10, 10), auth=False):
		if auth:
			data['jwt'] = self.jwt
		response = self.session.post(url, params=params, data=data, headers=headers,
									cookies=cookies, timeout=timeout)
		data = response.json()
		if not data['success']:
			raise ApiError(data['message'])
		return response

	def __repr__(self):
		return f"<Bot name='{self.name} password='{self.password}'>"


class BotFactory:

	def __init__(self):
		self._load_settings()
		self.bots = []
		self.load_bots_from_file()

	def _load_settings(self):
		with open('config.json', 'r') as file:
			self.settings = json.load(file)

	def load_bots_from_file(self, file_name="bots.json"):
		with open(file_name, 'r') as file:
			self.bots_info = json.load(file)

	def save_bots_to_file(self, file_name="bots.json"):
		with open(file_name, 'w') as file:
			json.dump(self.bots_info, file, indent=4)

	def init_bots_from_info(self):
		for bot in self.bots_info:
			new_bot = Bot(name=bot['name'], password=bot['password'])
			self.bots.append(new_bot)

	def add_bot(self, bot):
		self.bots.append(bot)
		self.bots_info.append(bot.get_info())
		self.save_bots_to_file()

	def start(self):
		self.init_bots_from_info()

		bots = []
		print("Start creating bots and posts...")
		for user_ind in range(self.settings['number_of_users']):
			bot = Bot()
			self.add_bot(bot)
			bots.append(bot)
			thread = Thread(target=self._do_task, args=(bot, ))
			thread.start()
			sleep(0.1)

		print("Bots has been created successfully")
		sleep(5)
		print("Start likes posts...")
		for bot in bots:
			thread = Thread(target=self._like_random_posts, args=(bot, ))
			thread.start()
			sleep(0.1)

	def _do_task(self, bot):
		bot.create_account()
		bot.do_login()
		# TODO: Make requests more 'human' by adding sleep
		posts_number = randint(1, self.settings['max_posts_per_user'])
		for post_ind in range(posts_number):
			bot.create_post()
			# sleep(0.1)

	def _like_random_posts(self, bot):
		likes_number = randint(1, self.settings['max_likes_per_user'])
		posts_amount = len(bot.get_all_posts())
		if likes_number > posts_amount:
			likes_number = posts_amount
		posts_ids = sample(range(1, posts_amount + 1), likes_number)
		for post_id in posts_ids:
			print(f"Bot: {bot} Post: {post_id}")
			bot.like_post(post_id)
			# sleep(0.1)