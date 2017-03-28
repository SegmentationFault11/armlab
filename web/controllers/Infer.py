from flask import *
from AccessManagement import login_required
from LcmClient import lcm_client
from Utilities import check_text_input
import os, logging

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
				speech_input = form['speech_input'] if 'speech_input' in form \
					else ''
				check_text_input(speech_input)
				logging.debug('Speech input: %s' % speech_input)
				options['result'] = lcm_client.send_to_backend(username, speech_input)
				logging.debug('Result: %s' % options['result'])
			else:
				raise RuntimeError('Did you click the Ask button?')
	except Exception as e:
		logging.error(e)
		options['error'] = e
		return render_template('infer.html', **options)
	# Display.
	return render_template('infer.html', **options)
