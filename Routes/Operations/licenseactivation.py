from werkzeug import secure_filename
from FlaskServer import app
from FlaskServer import radlogger
from FlaskServer.jsonutils import *
from FlaskServer.utils import *
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.attributeshelper as attributeshelper
import copy, os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def license_activation(req):
    if req.method == 'GET':
        try:

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributeshelper.LICENSE_ACTIVATION)
            status = ubus_attributes_dict[attributeshelper.LICENSE_ACTIVATION[ubuscontroller.NAME_KEY]]

            if status:          
                data = {}
                data['status'] = status

                # Wrap data
                response_json = wrap_data(data)

                return response_json

        except:
            radlogger.log('license_activation GET method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

    if req.method == 'POST':
        try:
            license_key = None

            if 'key' in req.args:
                license_key = req.args['key']

            if license_key:
                license_attr = copy.deepcopy(attributeshelper.LICENSE_ACTIVATION)
                license_attr['value'] = license_key
                ubus_attributes_dict = ubuscontroller.set_attributes_ubus(license_attr)
                status = ubus_attributes_dict[attributeshelper.LICENSE_ACTIVATION[ubuscontroller.NAME_KEY]]

                data = {}
                data['status'] = status

                # Wrap data
                response_json = wrap_data(data)

                return response_json

            response_json = wrap_data({}, error="Error occurred")
            return response_json
        except:
            radlogger.log('license_activation POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json
