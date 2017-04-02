from Service import Service

# Pre-configured services.
# The LcmClient assumes that the following services are running.
SERVICES = { 
	'ARM' : Service('ARM', 'localhost', 'LCM port'),
	'CAMERA' : Service('CAMERA', 'localhost', 12000)
	}

# Ingredients.
INGREDIENTS = ['Vodka', 'Orange Juice', 'Apple Juice', 'Water']

# Bottles.
BOTTLES = [0, 1, 2, 3]

# Maximum volume in ml.
MAX_ML = 150

# Time (sec) to open the valve for each ml.
SEC_PER_ML = 3.0 / 125.0

# Check.
assert(len(INGREDIENTS) == len(BOTTLES))
assert(SEC_PER_ML >= 0)
