from Database import database
import os, Config, sys
reload(sys)
sys.setdefaultencoding('utf8') # to solve the unicode error


class LcmClient(object):
	def send_to_backend(self, username, speech_input):
		recipes = database.get_recipes(username)
		if not recipes:
			return 'You don\'t have any recipes'
		else:
			drinkname = ''
			found = False
			for i in recipes:
				if i['drinkname'].lower() in speech_input.lower():
					if found:
						raise RuntimeError('Find two drinks %s and %s' % \
							(drinkname, i['drinkname']))
					found = True
					drinkname = str(i['drinkname'])
			if not found:
				raise RuntimeError('Canot find any drink')
			# Call camera controller.
			# Call arm controller.
			return '%s Being prepared...' % drinkname


lcm_client = LcmClient()
