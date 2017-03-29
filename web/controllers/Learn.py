from flask import Blueprint, session, render_template, request
import Database
from AccessManagement import login_required
from Database import database 
from LcmClient import lcm_client
from Utilities import get_text_input, logger
from Config import INGREDIENTS, MAX_ML


learn = Blueprint('learn', __name__, template_folder='templates')

# Checks if the ingredient amount is valid.
# Returns the amount as a float if so.
def get_amount(ingredient):
	rtn = float(get_text_input(ingredient))
	if rtn < 0:
		raise RuntimeError('Negative amount is not allowed')
	return rtn

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
				drinkname = get_text_input(form['drinkname'])
				if database.recipe_exists(username, drinkname):
					raise RuntimeError('Drink ' + drinkname + ' already exists')
				# Example ingredients: [('water', 0.0), ('vodka', 10.0)].
				ingredients = [(ingredient, get_amount(form[ingredient])) \
				for ingredient in INGREDIENTS]
				check_total_amount(ingredients)
				logger.debug('New ingredients: %s' % ingredients)
				# Add the recipe into the database.
				database.add_recipe(username, drinkname, ingredients)
			# Delete a recipe.
			elif form['op'] == 'delete_recipe':
				# Delete the recipe from into the database.
				database.delete_recipe(username, form['drinkname'])			
			else:
				raise RuntimeError('Did you click the button?')
	except Exception as e:
		logger.error(e)
		options['error'] = e
	# Retrieve recipes even if POST request fails.
	try:
		options['recipes'] = database.get_recipes(username)
		options['ingredients'] = INGREDIENTS
	except Exception as e:
		logger.error(e)
		options['error'] = e
	return render_template('learn.html', **options)
