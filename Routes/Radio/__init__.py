from FlaskServer.jsonutils import *
from FlaskServer.utils import *
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import FlaskServer.attributeshelper as attributeshelper
import os, sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
NUM_OF_EXISTING_SBW = 7   # 5,10,20,40,80,7,14
EXISTING_CBW = [5,10,20,40,80,7,14];

def radio_route(req):
    # Load mapping JSON file
    data = load_mapping_json_file(os.path.join(__location__, 'radio.json'))
        
    flatten_data = flatten_json(data)

    if req.method == 'GET':
        try:
            attributes_list = [attributeshelper.CAPABILITY_BITMASK]
                   
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            latitude = '0'
            longitude = '0'

            capabilityBitmask     = ubus_attributes_dict[attributeshelper.CAPABILITY_BITMASK[ubuscontroller.NAME_KEY]]
            isDynamicCbwSupported = getFetureSupportByCapability(capabilityBitmask, consts.CAPABILITY_INDEX_DYNAMIC_CHANNEL_BANDWIDTH)

            available_cbw = []
            cbw_table_data = load_mapping_json_file(os.path.join(__location__, 'cbwTable.json'))
            inflate_table(cbw_table_data, NUM_OF_EXISTING_SBW, 1)
            flatten_cbw_table_data = flatten_json(cbw_table_data)
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_cbw_table_data)
            for index in range(1, NUM_OF_EXISTING_SBW):
                key = 'cbwAvailable_' + str(index)
                if key in ubus_attributes_dict:
                    val = int(ubus_attributes_dict[key])
                    if (val > 1):
                        available_cbw.append(EXISTING_CBW[index-1])

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_data)
            
            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            # Casting
            cast_to_int_divide_by_factor(ubus_attributes_dict, 1000, 'currentCbw')
            cast_to_int_divide_by_factor(ubus_attributes_dict, 10, 'antennaGain', 'cableLoss', 'maxAntennaGain', 'minAntennaGain')
            cast_to_int(ubus_attributes_dict, 'minTxPower', 'maxTxPower', 'desiredTxPower')

            if isDynamicCbwSupported:
                cbw_in_auto_mode = ''
                for cbw in available_cbw:
                    if cbw > 10:
                        cbw_in_auto_mode = cbw_in_auto_mode + str(cbw) + "/"
                cbw_in_auto_mode =  cbw_in_auto_mode[:-1]
                cbw_in_auto_mode = 'Auto(' + cbw_in_auto_mode +')'
                available_cbw = ['10', cbw_in_auto_mode]
                # Set current CBW in auto mode
                if ubus_attributes_dict['currentCbw'] > 10:
                    ubus_attributes_dict['currentCbw'] = cbw_in_auto_mode


            if 'currentFrequency' in ubus_attributes_dict and ubus_attributes_dict['currentFrequency']:
                ubus_attributes_dict['currentFrequency'] = formatFrequency(ubus_attributes_dict['currentFrequency'])

            if 'antennaType' in ubus_attributes_dict and ubus_attributes_dict['antennaType']:
                ubus_attributes_dict['antennaType'] = converters.ANTENNA_TYPE[ubus_attributes_dict['antennaType']]

            if 'antennaConnectionType' in ubus_attributes_dict and ubus_attributes_dict['antennaConnectionType']:
                ubus_attributes_dict['antennaConnectionType'] = converters.ANTENNA_CONNECTION_TYPE[ubus_attributes_dict['antennaConnectionType']]

            if 'hsuType' in ubus_attributes_dict and ubus_attributes_dict['hsuType']:
                ubus_attributes_dict['hsuType'] = converters.SERVICE_HSU_TYPE[ubus_attributes_dict['hsuType']]

            if 'geoLocation' in ubus_attributes_dict and ubus_attributes_dict['geoLocation']:
                latLon = ubus_attributes_dict['geoLocation'].split(',')
                if (len(latLon) > 1):
                    latitude = latLon[0]
                    longitude = latLon[1]

            # Build response
            match_json(data, ubus_attributes_dict)
            data['options']['cbwList'] = available_cbw
            data.pop('geoLocation', None)
            data['latitude'] = latitude
            data['longitude'] = longitude

            response_json = wrap_data(data)
            return response_json

        except:
            print('radio_route(GET) - Unexpected error:', sys.exc_info()[0])
            response_json = wrap_data(None, error="Error occurred")
            return response_json

    if req.method == 'POST':
        try:
            
            # Get POST payload
            payload = req.get_json()

            payload_dict = flatten_payload_to_dict(payload)

            # Automatic CBW support
            if 'currentCbw' in payload_dict and 'Auto' in payload_dict['currentCbw']:
                payload_dict['currentCbw'] = 20
            # End Of Automatic CBW support

            cast_to_int_multiply_by_factor(payload_dict, 10, 'cableLoss', 'antennaGain')
            cast_to_int_multiply_by_factor(payload_dict, 1000, 'currentCbw')

            for attr in flatten_data:
                if attr[ubuscontroller.NAME_KEY] in payload_dict:
                    attr[ubuscontroller.VALUE_KEY] = payload_dict[attr[ubuscontroller.NAME_KEY]]

            flatten_data = [item for item in flatten_data if ubuscontroller.VALUE_KEY in item]

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(flatten_data)

            response_json = wrap_data(payload)

            return response_json

        except:
            print('radio_route(POST) - Unexpected error:', sys.exc_info()[0])
            response_json = wrap_data(None, error="Error occurred")
            return response_json
