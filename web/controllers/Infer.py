from flask import Blueprint, session, render_template, request
from AccessManagement import login_required
from LcmClient import lcm_client
from Utilities import get_text_input, logger
from Speech import tell_joke, JOKES
from time import sleep
import os, inspect, serial


infer = Blueprint('infer', __name__, template_folder='templates')

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
ser.isOpen()

def is_pressure_sensor_occupied():
	ser.write('w')
	sleep(0.1)
	result = ser.read()
	logger.debug('Pressure sensor result: %s' % result)  
	if result == 'G':
		return False
	elif result == 'B':
		return True
	else:
		raise RuntimeError('Pressure sensor result: %s' % result)

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
				# Check pressure sensor.
				if is_pressure_sensor_occupied():
					raise RuntimeError('Please place an empty cup on the gripper')
				# # Classify the query.
				speech_input = get_text_input(form['speech_input'] if \
					'speech_input' in form else '')
				logger.debug('Speech input: %s' % speech_input)
				options['result'] = lcm_client.send_to_backend(username, \
					speech_input)
				tell_joke()
				logger.debug('Result: %s' % options['result'])
			else:
				raise RuntimeError('Did you click the Ask button?')
	except Exception as e:
		logger.exception(e)
		options['result'] = e
		return render_template('infer.html', **options)
	# Display.
	return render_template('infer.html', **options)
