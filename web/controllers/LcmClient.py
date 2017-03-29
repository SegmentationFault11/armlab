from Database import database
import lcm, os, inspect, sys
from Config import SEC_PER_ML
from Utilities import logger
# Import LCM packages
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 
from lcm_python.arm_command_t import arm_command_t


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
					drink['ingred_amounts'] = self.prune_ingredients( \
						i['ingredients'])
			if not found:
				return 'What drink do you want?'
			# Call arm controller.
			msg = arm_command_t()
			msg.size = len(drink['ingred_amounts'])
			msg.hole_indices = self.get_hole_indices(drink)
			msg.stop_times = self.volume_to_time(drink['ingred_amounts'])
			logger.debug('LCM publishing:\n%s' % \
				self.msg_to_str(msg))
			#self.lc.publish("ARM", msg.encode())
			return '%s is being prepared...' % drink['drinkname']

	def prune_ingredients(self, ingredients):
		# If ingredients == [('vodka', 0.0), ('orange juice', 2.5)],
		# return [2.5].
		return [i[1] * SEC_PER_ML for i in ingredients if i[1] > 0]

	def get_hole_indices(self, drink):
		# Call camera controller.
		return range(len(drink['ingred_amounts']))

	def volume_to_time(self, ingred_amounts):
		# If ingred_amounts == [2.5],
		# return [2.5 * SEC_PER_ML].
		return [i * SEC_PER_ML for i in ingred_amounts]

	def msg_to_str(self, msg):
		assert(msg.size == len(msg.hole_indices) == len(msg.stop_times))
		return '%s\n%s\n%s' % (msg.size, msg.hole_indices, msg.stop_times)

lcm_client = LcmClient()
