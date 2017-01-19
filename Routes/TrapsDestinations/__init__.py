from FlaskServer.jsonutils import *
from FlaskServer.utils import *
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def trapsdestinations_route(req):

    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'trapsdestinations.json'))

    number_of_traphosts = 10
            
    # Add rows to table and update proper index
    inflate_table(data, int(number_of_traphosts))

    flatten_data = flatten_json(data)

    if req.method == 'GET':
        attributes_list = []
        try:

            # Send list to ubus
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)

            # Go over json data and match values received from ubus
            match_json(data, ubus_attributes_dict)

            # Wrap data
            response_json = wrap_data(data)

            return response_json

        except:
            radlogger.log('trapsdestinations_route GET method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

    if req.method == 'POST':
        try:

            # Get POST payload
            payload = req.get_json()

            payload_dict = flatten_payload_to_dict(payload)

            for attr in flatten_data:
                if attr[ubuscontroller.NAME_KEY] in payload_dict:
                    attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

            flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

            response_json = wrap_data(payload)

            return response_json

        except:
            radlogger.log('trapsdestinations_route POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json
