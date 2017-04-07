from flask import Blueprint, render_template, session, request
from AccessManagement import login_required
from Database import database 
from Utilities import get_text_input, logger


create = Blueprint('create', __name__, template_folder='templates')

# Checks if the april tag id is valid.
# Returns the id as an int if so.
def get_april_id(form):
	rtn = get_text_input(form['april_id'])
	if not rtn.isdigit():
		raise RuntimeError('April Tag ID must be in integer')
	rtn = int(rtn)
	return rtn


@create.route('/create', methods=['GET', 'POST'])
@login_required
def create_route():
	options = {}
	username = session['username']
	try:
		form = request.form
		# Deal with POST requests.
		if request.method == 'POST':
			# If the request does not contain an "op" field.
			if not 'op' in request.form:
				raise RuntimeError('Did you click the button?')
			# Add a ingredient.
			elif form['op'] == 'add_ingred':
				ingred_name = get_text_input(form['ingred_name'])
				april_id = get_april_id(form)
				database.check_ingred_april_id(username, ingred_name, april_id)
				logger.debug('New ingredient: %s at April Tag %s' % \
					(ingred_name, april_id))
				# Add the ingredient into the database.
				database.add_ingredient(username, ingred_name, april_id)
			# Delete an ingredient.
			elif form['op'] == 'delete_ingred':
				# Delete the ingredient from the database.
				database.delete_ingredient(username, form['ingred_name'])			
			else:
				raise RuntimeError('Did you click the button?')
	except Exception as e:
		logger.exception(e)
		options['error'] = e
	# Retrieve ingredients even if POST request fails.
	try:
		options['ingredients'] = database.get_ingredients(username)
	except Exception as e:
		logger.exception(e)
		options['error'] = e
	return render_template('create.html', **options)
