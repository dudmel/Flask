from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer.Resources import en as resource
from FlaskServer import radlogger
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def wifi_route(req):

    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'wifi.json'))

    # Add rows to table and update proper index
    #if req.method == 'GET':
    #    inflate_table(data['wifiRssiTable'], 5)

    flatten_data = flatten_json(data)

    if req.method == 'GET':
        try:

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            #cast_to_int(ubus_attributes_dict,'wifiChannel', 'wifiTxPower')
            cast_to_int(ubus_attributes_dict,'wifiChannel')

            if 'wifiMode' in ubus_attributes_dict and ubus_attributes_dict['wifiMode']:
                ubus_attributes_dict['wifiMode'] = converters.WIFI_POWER_MODES[ubus_attributes_dict['wifiMode']]
                if ubus_attributes_dict['wifiMode'] == resource.wifi_power_on:
                    ubus_attributes_dict['wifiMode'] = resource.wifi_auto

            if 'wifiSecurityType' in ubus_attributes_dict and ubus_attributes_dict['wifiSecurityType']:
                ubus_attributes_dict['wifiSecurityType'] = converters.WIFI_SECURITY_TYPE[ubus_attributes_dict['wifiSecurityType']]

            # Moved to monitor
            #if 'wifiApStatus' in ubus_attributes_dict and ubus_attributes_dict['wifiApStatus']:
            #    ubus_attributes_dict['wifiApStatus'] = converters.WIFI_AP_STATUS[ubus_attributes_dict['wifiApStatus']]

            # Build response
            match_json(data, ubus_attributes_dict)

            #pop wifi password
            data.pop('wifiPassword', None)

            response_json = wrap_data(data)
            
            return response_json

        except:
            radlogger.log('wifi_route GET method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

    if req.method == 'POST':
        try:
            
            # Get POST payload
            payload = req.get_json()          

            payload_dict = flatten_payload_to_dict(payload)

            if 'wifiMode' in payload_dict and payload_dict['wifiMode'] != '0':
                payload_dict['wifiMode'] = converters.WIFI_POWER_MODES[payload_dict['wifiMode']]

            for attr in flatten_data:
                if attr[ubuscontroller.NAME_KEY] in payload_dict:
                    attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

            flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

            response_json = wrap_data(payload)

            return response_json

        except:
            radlogger.log('wifi_route POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json
