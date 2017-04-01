import socket
import sys

def get_bottle_locations(ip = 'localhost'):
	camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	camera_socket.connect(('localhost', 12000))

	camera_socket.send("Get Locations" + '\0')

	print camera_socket.recv(512)

def calibrate_slot_locations(calibration_string):
	camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	camera_socket.connect(('localhost', 12000))

	camera_socket.send("Calibrate Locations " + calibration_string + '\0')

	print camera_socket.recv(512)

if len(sys.argv) > 1:
	get_bottle_locations(sys.argv[1])
else:
	get_bottle_locations()
