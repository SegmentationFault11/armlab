import hashlib, uuid
from pymongo import MongoClient
from base64 import b64encode
from Utilities import logger
import os, logging, Config


class Database(object):
	# Name of the algorithm to use for password encryption.
	ENCRYPT_ALGORITHM = 'sha512'
	
	# Constructor.
	def __init__(self):
		mongodb_addr = os.environ.get('MONGO_PORT_27017_TCP_ADDR')
		if mongodb_addr:
			logger.INFO('MongoDB: ' + mongodb_addr)
			self.db = MongoClient(mongodb_addr, 27017).barman
		else:
			logger.info('MongoDB: localhost')
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

	# Adds the ingredient name and its april tag id.
	def add_ingredient(self, username, ingred_name, april_id):
		self._get_ingredient_collection(username).insert_one( \
			{'ingred_name': ingred_name, 'april_id': april_id})

	# Checks if the ingredient name and its april tag id are valid.
	# Throws exception otherwise.
	def check_ingred_april_id(self, username, ingred_name, april_id):
		ingred_collection = self.get_ingredients(username)
		for i in ingred_collection:
			if i['ingred_name'] == ingred_name:
				raise RuntimeError('Ingredient already exists')
			if i['april_id'] == april_id:
				raise RuntimeError('April Tag ID already associated with %s' % \
					i['ingred_name'])

	# Deletes the ingredient.
	def delete_ingredient(self, username, ingred_name):
		self._get_ingredient_collection(username).delete_one( \
			{'ingred_name': ingred_name})
		
	# Returns all the ingredients.
	def get_ingredients(self, username):
		logger.info('Retrieving ingredients from ingredient_' + username)
		return [ingredient for ingredient in \
		self._get_ingredient_collection(username).find()]

	# Returns all the ingredient names.
	def get_ingredient_names(self, username):
		logger.info('Retrieving ingredients from ingredient_' + username)
		return [ingredient['ingred_name'] for ingredient in \
		self._get_ingredient_collection(username).find()]

	# Returns the ingredient name corresponding to the april tag id.
	# Returns '' if the id doesn't correspond to any ingredient.
	def get_ingredient_name_from_id(self, username, april_id):
		logger.info('Finding ingredient name from april id ' + str(april_id))
		ingred_collection = self.get_ingredients(username)
		for i in ingred_collection:
			if i['april_id'] == april_id:
				return i['ingred_name']
		return ''

	# Returns the ingredient collection of the user.
	def _get_ingredient_collection(self, username):
		return self.db['ingredient_' + username]
	
	# Adds the recipe.
	def add_recipe(self, username, drinkname, ingredients):
		self._get_recipe_collection(username).insert_one( \
			{'drinkname': drinkname, 'ingredients': ingredients})

	# Returns true if the recipe already exists.
	def recipe_exists(self, username, drinkname):
		return not self._get_recipe_collection(username).find_one( \
			{'drinkname': drinkname}) is None
		
	# Deletes the recipe.
	def delete_recipe(self, username, drinkname):
		self._get_recipe_collection(username).delete_one( \
			{'drinkname': drinkname})
		
	# Returns all the recipes.
	def get_recipes(self, username):
		logger.info('Retrieving recipes from recipe_' + username)
		return [recipe for recipe in \
		self._get_recipe_collection(username).find()]

	# Returns the recipe collection of the user.
	def _get_recipe_collection(self, username):
		return self.db['recipe_' + username]

database = Database()
