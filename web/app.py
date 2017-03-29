import sys, logging
from flask import Flask

def setup_logging():
	log = logging.getLogger('log')
	log.setLevel(logging.DEBUG)
	format = logging.Formatter('127.0.0.1 - - [%(asctime)s] %(levelname)s in ' \
		'[%(filename)s:%(lineno)d]: %(message)s','%m/%d/%y %H:%M:%S')
	ch = logging.StreamHandler(sys.stdout)
	ch.setFormatter(format)
	log.addHandler(ch)

setup_logging()

from controllers import *

# Initialize the Flask app with the template folder address.
app = Flask(__name__, template_folder='templates')

# Register the controllers.
app.register_blueprint(Main.main)
app.register_blueprint(User.user)
app.register_blueprint(Create.create)
app.register_blueprint(Learn.learn)
app.register_blueprint(Infer.infer)

# Cryptographic components can use this to sign cookies.
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def flask_listener():
	app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=False,
			threaded=True)

if __name__ == '__main__':
	flask_listener()
