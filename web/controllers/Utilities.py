from werkzeug import secure_filename
from threading import Lock


print_lock = Lock()

def log(s):
	print_lock.acquire()
	print(s)
	print_lock.release() 

# Checks if the text input is valid.
def check_text_input(text_input):
	if text_input is None:
		return
	if len(text_input) >= 200:
		raise RuntimeError('Please input less than 200 characters')
	if (text_input == '') or text_input.isspace():
		raise RuntimeError('Empty text is not allowed')
