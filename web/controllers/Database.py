import hashlib, uuid
from pymongo import MongoClient
from base64 import b64encode
from Utilities import log
import os
import Config


class Database(object):
	# Name of the algorithm to use for password encryption.
	ENCRYPT_ALGORITHM = 'sha512'
	
	# Constructor.
	def __init__(self):
		mongodb_addr = os.environ.get('MONGO_PORT_27017_TCP_ADDR')
		if mongodb_addr:
			log('MongoDB: ' + mongodb_addr)
			self.db = MongoClient(mongodb_addr, 27017).barman
		else:
			log('MongoDB: localhost')
			self.db = MongoClient().barman
		self.users = self.db.users
	
	# Adds a new user.
	def add_user(self, username, firstname, lastname, password, email):
		salt = uuid.uuid4().hex # thwart rainbow attack
		hashed_password = self.hash_password(self.ENCRYPT_ALGORITHM, \
			salt, password)
		self.users.insert_one({'username' : username,
			'firstname': firstname, 'lastname': lastname,
			'password': hashed_password, 'email': email})
	
	# Returns true if password of the user is correct
	def check_password(self, username, input_password):
		correct_password_in_db = (self.users.find_one
			({'username': username}))['password']
		salt = correct_password_in_db.split('$')[1]
		generated_password = self.hash_password(self.ENCRYPT_ALGORITHM, \
			salt, input_password)
		return correct_password_in_db == generated_password
	
	# Generates a hashed password from the raw password.
	def hash_password(self, algorithm, salt, password):
		m = hashlib.new(algorithm)
		password = password.encode('utf-8')
		s = salt + password
		m.update(s)
		password_hash = m.hexdigest()
		return "$".join([algorithm, salt, password_hash])
	
	# Returns true if the username already exists.
	def username_exists(self, username):
		return not self.users.find_one({'username': username}) is None
	
	# Adds the recipe.
	def add_recipe(self, username, drinkname, ingredients):
		self.get_recipe_collection(username).insert_one( \
			{'drinkname': drinkname, 'ingredients': ingredients})

	# Returns true if the recipe already exists.
	def recipe_exists(self, username, drinkname):
		return not self.get_recipe_collection(username).find_one( \
			{'drinkname': drinkname}) is None
		
	# Deletes the recipe.
	def delete_recipe(self, username, drinkname):
		self.get_recipe_collection(username).delete_one( \
			{'drinkname': drinkname})
		
	# Returns all the recipes.
	def get_recipes(self, username):
		log('Retrieving recipes from recipe_' + username)
		return [recipe for recipe in self.get_recipe_collection(username).find()]

	# Returns the recipe collection of the user.
	def get_recipe_collection(self, username):
		recipe_collection = 'recipe_' + username
		return self.db[recipe_collection]

database = Database()
