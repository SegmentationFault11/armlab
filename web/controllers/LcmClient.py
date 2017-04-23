from Database import database
import lcm, os, inspect, sys, socket
from Config import SEC_PER_ML
from Utilities import logger
# Import LCM packages
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 
from lcm_python.arm_command_t import arm_command_t


DEBUG = False

class LcmClient(object):
	def __init__(self):
		self.lc = lcm.LCM()

	def send_to_backend(self, username, speech_input):
		recipes = database.get_recipes(username)
		if not recipes:
			return 'You don\'t have any recipes'
		else:
			drink = {}
			found = False
			for i in recipes:
				if i['drinkname'].lower() in speech_input.lower():
					if found:
						return 'Find two drinks %s and %s' % \
							(drink['drinkname'], i['drinkname'])
					found = True
					logger.debug('Drink to prepare: %s' % i)
					drink['drinkname'] = str(i['drinkname'])
					drink['ingred_amounts'], drink['ingred_names'] = \
					self.prune_ingredients(i['ingredients'])
			if not found:
				return 'What drink do you want?'
			assert(len(drink['ingred_amounts']) == len(drink['ingred_names']))
			logger.debug('Drink to prepare (pruned): %s' % drink)
			# Call arm controller.
			msg = arm_command_t()
			msg.size = len(drink['ingred_amounts'])
			msg.hole_indices = self.get_hole_indices(drink['ingred_names'], \
				username)
			msg.stop_times = self.volume_to_time(drink['ingred_amounts'])
			logger.debug('LCM publishing:\n%s' % \
				self.msg_to_str(msg))
			if not DEBUG:
				self.lc.publish("ARM", msg.encode())
			return '%s is being prepared...' % drink['drinkname']

	def prune_ingredients(self, ingredients):
		# If ingredients == [('Vodka', 0.0), ('Orange Juice', 2.5)],
		# return [2.5], ['Orange Juice'].
		return [i[1] for i in ingredients if i[1] > 0], \
		[i[0] for i in ingredients if i[1] > 0]

	def get_hole_indices(self, ingred_names, username):
		# Call camera controller.
		# If ingred_names == ['Orange Juice'],
		# return [<hole_id>].
		if not DEBUG:
			try:
				camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				camera_socket.connect(('35.2.227.11', 12000))
				camera_socket.send("Get Locations" + '\0')
				rcv = camera_socket.recv(512)
			except Exception as e:
				raise RuntimeError('Camera\'s error: ' + str(e) + '. Please ask SM for help.')
		else:
			rcv = '{7|2}{5|0}{4|1}'
		logger.debug('Camera returns: %s' % rcv)
		ingred_hole_map = self.parse_camera_rcv(rcv, username)
		logger.debug('Mapping btw ingredients and holes: %s' % ingred_hole_map)
		rtn = []
		for ingred_name in ingred_names:
			if not ingred_name in ingred_hole_map:
				raise RuntimeError(ingred_name + ' is not in stock')
			rtn.append(ingred_hole_map[ingred_name])
		return rtn

	def parse_camera_rcv(self, rcv, username):
		# ...{hole_id|april_id}...
		# If rcv == '{7|2}{5|0}{4|1}', (assuming single-digit)
		# return {'Apple Juice': 7, 'Vodka': 5, 'Orange Juice': 4}.
		if 'FATAL' in rcv:
			raise RuntimeError(rcv)
		rtn = {}
		ingred_name = ''
		hole_id = 0
		state = 0
		for c in rcv:
			if state == 0:
				assert(c == '{')
				state = 1
			elif state == 1:
				hole_id = int(c)
				state = 2
			elif state == 2:
				assert(c == '|')
				state = 3
			elif state == 3:
				april_id = int(c)
				assert(april_id >= 0)
				ingred_name = database.get_ingredient_name_from_id(username, \
					april_id)
				state = 4
			elif state == 4:
				assert(c == '}')
				rtn[ingred_name] = hole_id
				state = 0
			else:
				assert False
		return rtn

	def volume_to_time(self, ingred_amounts):
		# If ingred_amounts == [2.5],
		# return [2.5 * SEC_PER_ML].
		return [i * SEC_PER_ML for i in ingred_amounts]

	def msg_to_str(self, msg):
		assert(msg.size == len(msg.hole_indices) == len(msg.stop_times))
		return '%s\n%s\n%s' % (msg.size, msg.hole_indices, msg.stop_times)

lcm_client = LcmClient()
