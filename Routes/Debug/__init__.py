import FlaskServer.ubuscontroller as ubuscontroller
from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import app
from flask import send_file
import os.path
import glob

CUSTOM_ATTRIBUTE = 'custom'

def debug_log_route():
        try:
            
            # Get all log file app.log, app.log.1, etc..
            filelist = glob.glob(app.root_path + '/*.log*')
            temp_log_file = app.root_path + '/temp.log'

            # Delete concatenated temp file
            if os.path.exists(temp_log_file):
                os.remove(temp_log_file)

            # Concatenate all log files
            with open(app.root_path + '/temp.log', 'w') as outfile:
                for fname in filelist:
                    with open(fname) as infile:
                        outfile.write(infile.read())
            
            # Send file
            if os.path.exists(temp_log_file):
                return send_file(temp_log_file, mimetype='text/plain')
            else:
                return None

        except:
            radlogger.log('debug_log_route method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

def debug_attribute_route(req):
        try:
           
            ubus_transaction = {}
            ubus_transaction[ubuscontroller.OBJECT_KEY] = int(req.args[ubuscontroller.OBJECT_KEY])
            ubus_transaction[ubuscontroller.ATTR_KEY] = int(req.args[ubuscontroller.ATTR_KEY])
            ubus_transaction[ubuscontroller.INDEX_KEY] = int(req.args[ubuscontroller.INDEX_KEY])
            ubus_transaction[ubuscontroller.NAME_KEY] = CUSTOM_ATTRIBUTE

            if req.method == 'GET':
                ubus_attributes_dict = ubuscontroller.get_attributes_ubus([ubus_transaction])
            
            if req.method == 'POST':
                ubus_transaction[ubuscontroller.VALUE_KEY] = req.args[ubuscontroller.VALUE_KEY].encode('utf-8')
                ubus_attributes_dict = ubuscontroller.set_attributes_ubus([ubus_transaction])
            
            response_json = wrap_data(ubus_attributes_dict[CUSTOM_ATTRIBUTE])

            return response_json

        except:
            radlogger.log('debug_attribute_route method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

