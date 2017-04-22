from flask import Blueprint, session, render_template, request
from AccessManagement import login_required
from LcmClient import lcm_client
from Utilities import get_text_input, logger
from Speech import tell_joke_wrapper, JOKES
from random import randint
import os, inspect


infer = Blueprint('infer', __name__, template_folder='templates')

@infer.route('/infer', methods=['GET', 'POST'])
@login_required
def infer_route():
	options = {}
	username = session['username']
	if os.environ.get('ASR_ADDR_PO`RT'):
		options['asr_addr_port'] = os.environ.get('ASR_ADDR_PORT')
	else:
		options['asr_addr_port'] = 'ws://localhost:8081'
	try:
		form = request.form
		# Deal with POST requests.
		if request.method == 'POST':
			# If the request does not contain an "op" field.
			if not 'op' in form:
				raise RuntimeError('Did you click the Ask button?')
			# When the "op" field is equal to "infer".
			elif form['op'] == 'infer':
				# # Classify the query.
				speech_input = get_text_input(form['speech_input'] if \
					'speech_input' in form else '')
				logger.debug('Speech input: %s' % speech_input)
				options['result'] = lcm_client.send_to_backend(username, speech_input)
				tell_joke_wrapper(randint(0, len(JOKES)-1))
				logger.debug('Result: %s' % options['result'])
			else:
				raise RuntimeError('Did you click the Ask button?')
	except Exception as e:
		logger.exception(e)
		options['error'] = e
		return render_template('infer.html', **options)
	# Display.
	return render_template('infer.html', **options)
