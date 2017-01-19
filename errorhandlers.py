import sys
from flask import jsonify, request
from FlaskServer.utils import *
import logging

def configure_error_handlers(app):
	
	@app.errorhandler(400)
	def bad_request(error):
		app.logger.error('Bad request: %s', (request.path, error))
		return render_error(400, 'Bad request')

	@app.errorhandler(404)
	def route_not_found(error):
		app.logger.error('Route not found: %s', (request.path, error))
		return render_error(404, 'Route not found')

	@app.errorhandler(405)
	def method_not_allowed(error):
		app.logger.error('Method not allowed: %s', (request.path, error))
		return render_error(405, 'Method not allowed')

	@app.errorhandler(500)
	def internal_server_error(error):
		app.logger.error('Server Error: %s', (error))
		return render_error(500, 'Server Error')

	@app.errorhandler(Exception)
	def unhandled_exception(error):
		app.logger.exception('Unhandled Exception: %s', (error))
		if 'Signature has expired' in str(error):
			return render_error(401, 'Invalid token. Signature has expired', True)
		if 'Request does not contain an access token' in str(error):
			return render_error(401, 'Authorization Required. Request does not contain an access token', True)
		if '"Invalid credentials' in str(error):
			return render_error(401, 'Bad Request. Invalid credentials', True)
		return render_error(500, 'Server Error')

def render_error(error, errorMsg, httpError=None):
	if httpError:
		return jsonify(wrap_data(None, error=errorMsg)), error
	else:
		return jsonify(wrap_data(None, error=errorMsg))
