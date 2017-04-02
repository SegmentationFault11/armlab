from Service import Service

# Pre-configured services.
# The LcmClient assumes that the following services are running.
SERVICES = { 
	'ARM' : Service('ARM', 'localhost', 'LCM port'),
	'CAMERA' : Service('CAMERA', 'localhost', 12000)
	}

# Ingredients.
INGREDIENTS = ['Vodka', 'Orange Juice', 'Apple Juice', 'Water', 'Purified Water']

# Maximum volume in ml.
MAX_ML = 150

# Time (sec) to open the valve for each ml.
SEC_PER_ML = 3.0 / 30.0

# Check.
assert(SEC_PER_ML >= 0)
if len(INGREDIENTS) > 10:
	raise RuntimeError('Too many ingredients but only 4 bottles')
assert(len(INGREDIENTS) == len(set(INGREDIENTS))) # check duplicate

