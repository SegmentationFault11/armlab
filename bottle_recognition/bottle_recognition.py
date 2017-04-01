import socket

def get_bottle_locations():
	camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	camera_socket.connect(('localhost', 12000))

	camera_socket.send("Get Locations" + '\0')

	print camera_socket.recv(100);

def calibrate_slot_locations(calibration_string):
	camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	camera_socket.connect(('localhost', 12000))

	camera_socket.send("Calibrate Locations " + calibration_string + '\0')

	print camera_socket.recv(100);

get_bottle_locations();
