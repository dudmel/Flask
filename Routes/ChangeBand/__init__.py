from FlaskServer.utils import *
from FlaskServer.jsonutils import *
from FlaskServer import radlogger
from FlaskServer.Routes.Operations import *
from threading import Timer

import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.attributeshelper as attributeshelper
import os, sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

RESET_TIMER = 5

def changeBand(req):
    if req.method == 'GET':
        attributes_list = []
        try:

            file_to_open = 'preChangeBand.json'
            pre_combo_requests = load_mapping_json_file(os.path.join(__location__, file_to_open))
                
            file_to_open = 'changeBand.json'
            combo_table_requests = load_mapping_json_file(os.path.join(__location__, file_to_open))

        except:
            radlogger.log('Unable to open ' + file_to_open + ' input data file.', sys.exc_info())
            response_json = wrap_data({}, error="Error Occurred")
            return response_json

        try:
            attributes_list = [attributeshelper.COMBO_NUMBER_OF_SUBBANDS, attributeshelper.CURRENT_SUB_BAND_ID]

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            number_of_subBands  = ubus_attributes_dict[attributeshelper.COMBO_NUMBER_OF_SUBBANDS['name']]
            current_sub_band_id = ubus_attributes_dict[attributeshelper.CURRENT_SUB_BAND_ID['name']]

            if not number_of_subBands:
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            inflate_table(pre_combo_requests, int(number_of_subBands), 0)   # WRNING!!! Zero Based table
                
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(pre_combo_requests))

            match_json(pre_combo_requests, ubus_attributes_dict)          
       
            default_combo_row = copy.deepcopy(combo_table_requests['bandsList'][0])
            combo_table_requests['bandsList'] = []
                       
            for band_index in range(0, int(number_of_subBands)):
                if pre_combo_requests[int(band_index)]['subBandAdminState'] == '1':
                    temp = copy.deepcopy(default_combo_row)
                    for key, val in temp.items():
                        val['index'] = band_index   # WRNING!!! Zero Based table
                    combo_table_requests['bandsList'].append(temp)
                band_index = band_index + 1

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(combo_table_requests))

            match_json(combo_table_requests, ubus_attributes_dict)

            response_json = wrap_data(combo_table_requests)

            return response_json
    
        except:
            radlogger.log('Error in changeBand GET method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

    if req.method == 'POST':
        try:
            # Get POST payload
            payload = req.get_json() 
            
            payload_dict = flatten_payload_to_dict(payload)

            attributes_list = [attributeshelper.CURRENT_SUB_BAND_ID]
            
            attributes_list[0]['value'] = payload_dict['currentBandId']

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(attributes_list)

            success = bool(ubus_attributes_dict)

            if success:
                # Reset ODU on another thread and return response to client
                Timer(RESET_TIMER, odu_reset, ()).start()
                response_json = wrap_data(payload, msg="Change Band Successfully")
                return response_json
            else: 
                response_json = wrap_data(payload, error="Unable to set value")
                return response_json
        except:
            radlogger.log('Error in changeBand POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json
