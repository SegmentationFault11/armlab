# Web

The web module performs the following functionalities:

- Sets up the web front end.
- Maintains a list of registered back-end services.
- Classifies and forwards front-end requests to the appropriate services.
- Returns requested information to the front end.

Specifically, `app.py` starts the Flask server (listening to front end)
and web socket ASR router (listening to front end).


## Major Dependencies

- [Flask](http://flask.pocoo.org/)
- [MongoDB](https://www.mongodb.com/)

For most dependencies, `pip install <name>` should work. For `MongoDB`,
refer to [this](http://treehouse.github.io/installation-guides/mac/mongo-mac.html) for Mac.

## Structure

- `controllers/`: web controllers, database module, utilities module, 
configuration file (`Config.py`), etc.
- `static/`: static contents of the web front end
- `templates/`: html Jinja templates
- `app.py`: top-level module
- `clear_db.sh`: script to clear MongoDB (only for testing)

## Run

In the terminal, start the Flask server,

```
python app.py
```

In another terminal, start the MongoDB,

```
mongod
```

Open your browser and go to `http://localhost:3000/`. 
Notice that the command center assumes that the services specified in `controllers/Config.py` are running.
Make sure to start those services as well.
