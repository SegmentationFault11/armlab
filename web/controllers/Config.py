from Service import Service

# The maximum number of texts or images for each user.
# This is to prevent the server from over-loading.
MAX_DOC_NUM_PER_USER = 30 # non-negative inetegr

# Pre-configured services.
# The ThriftClient assumes that the following services are running.
# Host IP addresses are resolved dynamically: 
# either set by Kubernetes or localhost.
SERVICES = { 
	'VALVE' : Service('VALVE', 8082, 'text', 'text'), 
	'ARM' : Service('ARM', 8083, 'text', 'text'),
	'CAMERA' : Service('CAMERA', 8084, 'image', None)
	}

# Ingredients.
INGREDIENTS = ['Vodka', 'Orange Juice', 'Apple Juice', 'Water']

# Maximum volume in ml.
MAX_ML = 150

# Time (sec) to open the valve for each ml.
SEC_PER_ML = 3.0 / 125.0
