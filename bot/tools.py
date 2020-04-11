import json
import requests
from random import choice, randint, sample


def load_data_from_file(file_name):
	with open(file_name, "r") as file:
		data = json.load(file)
	return data

def get_random_login():
	first = choice(data_first)
	last = choice(data_last)
	rand_int = randint(10, 99)
	return f"{first}{last}{rand_int}"

def get_firstname():
	first = choice(data_first)
	return first

def get_lastname():
	last = choice(data_last)
	return last

def get_number():
	rand_int = randint(10, 99)
	return rand_int

def generate_password(length=12):
	symbols = "0123456789001234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	noun = choice(data_nouns)[:8]
	symbols_extra = "".join(sample(symbols, length - len(noun)))
	password = f"{noun}{symbols_extra}"
	return password

data_first = load_data_from_file('files/first_names.json')
data_last = load_data_from_file('files/last_names.json')
data_nouns = load_data_from_file('files/english_words.json')