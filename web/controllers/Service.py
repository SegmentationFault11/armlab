class Service(object):
	# Constructor.
	def __init__(self, name, host, port):
		self.name = name
		self.host= host
		self.port = port
			
	def get_host_port(self):
		return self.host, self.port	
			
			