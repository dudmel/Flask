from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os, sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def system_route(req):

    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'system.json'))
        
    flatten_data = flatten_json(data)

    if req.method == 'GET':
        try:

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            # Build response
            match_json(data, ubus_attributes_dict)

            # Parse compressed data
            parsed_data = compresseddatahelper.parse_hsu_static(data['hbs']['hbsCompressedStatic'])
            if parsed_data:
                for val in parsed_data:
                    if val == 'hbsAntennaType':
                        data['hbs'][val] = converters.ANTENNA_TYPE[parsed_data[val]]
                    else:
                        data['hbs'][val] = parsed_data[val]
            else:
                data['hbs'] = {}

            # Sanitize data
            data['hbs'].pop('hbsCompressedStatic', None)

            response_json = wrap_data(data)
            
            return response_json

        except:
            radlogger.log('system_route GET method.', sys.exc_info())
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
            radlogger.log('system_route POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json
