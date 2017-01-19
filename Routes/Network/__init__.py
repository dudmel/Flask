from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import FlaskServer.attributeshelper as attributeshelper
import os, sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def network_route(req):

    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'network.json'))
        
    flatten_data = flatten_json(data)

    if req.method == 'GET':
        try:

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
            if not bool(ubus_attributes_dict):
                return None

            cast_to_int(ubus_attributes_dict, 'vlanId', 'vlanPriority', 'crcErrors')

            # Convert values in dict          
            if 'currentPortState' in ubus_attributes_dict and ubus_attributes_dict['currentPortState'] and ubus_attributes_dict['currentPortState'] != '0':
                ubus_attributes_dict['currentPortState'] = converters.LAN_CURRENT_STATUS[ubus_attributes_dict['currentPortState']]

            if 'desiredPortState' in ubus_attributes_dict and ubus_attributes_dict['desiredPortState'] and ubus_attributes_dict['desiredPortState'] != '0':
                ubus_attributes_dict['desiredPortState'] = converters.LAN_DESIRED_STATUS[ubus_attributes_dict['desiredPortState']]

            # Build response
            match_json(data, ubus_attributes_dict)

            response_json = wrap_data(data)
            
            return response_json

        except:
            radlogger.log('network_route GET method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

    if req.method == 'POST':
        try:
            
            # Get POST payload
            payload = req.get_json()          

            payload_dict = flatten_payload_to_dict(payload)

            _full_ip_param = ''
            # if all IP params exists concatenate them to use in ipParmas 
            if ('hsuIp' in payload_dict and payload_dict['hsuIp'] and
                'hsuSubnetMask' in payload_dict and payload_dict['hsuSubnetMask'] and
                'hsuDefaultGateway' in payload_dict and payload_dict['hsuDefaultGateway']):
                    _full_ip_param = '{0}|{1}|{2}|'.format(payload_dict['hsuIp'], payload_dict['hsuSubnetMask'], payload_dict['hsuDefaultGateway'])
                    payload_dict.pop('hsuIp', None)
                    payload_dict.pop('hsuSubnetMask', None)
                    payload_dict.pop('hsuDefaultGateway', None)

            if 'desiredPortState' in payload_dict and payload_dict['desiredPortState'] != '0':
                payload_dict['desiredPortState'] = converters.LAN_DESIRED_STATUS[payload_dict['desiredPortState']]

            for attr in flatten_data:
                if attr[ubuscontroller.NAME_KEY] in payload_dict:
                    attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

            flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]

            # Add ip param config
            if _full_ip_param:
                ip_attr = attributeshelper.IP_PARAMS_CONFIG
                ip_attr['value'] = _full_ip_param
                flatten_data.append(ip_attr)

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

            response_json = wrap_data(payload)

            return response_json

        except:
            radlogger.log('network_route POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json
