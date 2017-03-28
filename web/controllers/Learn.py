import hashlib, datetime, logging
from flask import *
import Database
from AccessManagement import login_required
from Database import database 
from LcmClient import lcm_client
from Utilities import check_text_input
from Config import INGREDIENTS, MAX_ML


learn = Blueprint('learn', __name__, template_folder='templates')

# Checks if the ingredient amount is valid.
# If so, returns the amount as a float.
def check_amount(ingredient):
	check_text_input(ingredient)
	return float(ingredient)

# Checks if the total amount of ingredients is within the limit.
def check_total_amount(ingredients):
	tot = 0.0
	for i in ingredients:
		tot += i[1]
	if tot > MAX_ML:
		raise RuntimeError('Total volume ' + str(tot) + ' is larger than ' + \
			str(MAX_ML))

@learn.route('/learn', methods=['GET', 'POST'])
@login_required
def learn_route():
	options = {}
	username = session['username']
	try:
		form = request.form
		# Deal with POST requests.
		if request.method == 'POST':
			# If the request does not contain an "op" field.
			if not 'op' in request.form:
				raise RuntimeError('Did you click the button?')
			# Add a recipe.
			elif form['op'] == 'add_recipe':
				drinkname = form['drinkname']
				check_text_input(drinkname)
				if database.recipe_exists(username, drinkname):
					raise RuntimeError('Drink ' + drinkname + ' already exists')
				ingredients = [(ingredient, check_amount(form[ingredient])) \
				for ingredient in INGREDIENTS]
				check_total_amount(ingredients)
				logging.debug('New drink ingredients: %s' % ingredients)
				# Add the recipe into the database.
				database.add_recipe(username, drinkname, ingredients)
			# Delete a recipe.
			elif form['op'] == 'delete_recipe':
				drinkname = form['drinkname']
				# Delete the recipe from into the database.
				database.delete_recipe(username, drinkname)			
			else:
				raise RuntimeError('Did you click the button?')
	except Exception as e:
		logging.error(e)
		options['error'] = e
	try:
		# Retrieve recipes.
		options['recipes'] = database.get_recipes(username)
		options['ingredients'] = INGREDIENTS
	except Exception as e:
		logging.error(e)
		options['error'] = e
	return render_template('learn.html', **options)
