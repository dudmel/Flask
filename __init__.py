"""
The flask application package.
"""
from flask import Flask
from flask_jwt import JWT
from werkzeug.contrib.cache import SimpleCache
from FlaskServer.config import configure_app
from FlaskServer.errorhandlers import configure_error_handlers

app = Flask(__name__)
app.cache = SimpleCache()

# Global configuration, debug, logging, keys, etc...
configure_app(app)

# Error handlers for 400, 404, 500 codes
configure_error_handlers(app)

# JWT
from FlaskServer.Authentication import authenticate, identity
jwt = JWT(app, authenticate, identity)

#import route for testing/prod
if app.config['TESTING_ROUTES_ENABLED']:
    from FlaskServer.utils import clean
    clean()
    import FlaskServer.testroutes
elif app.config['TRAINING_ROUTES_ENABLED']:
    import FlaskServer.trainingroutes
else:
    import FlaskServer.prodroutes
