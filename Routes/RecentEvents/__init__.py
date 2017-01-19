from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
import FlaskServer.consts as consts
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.attributeshelper as attributeshelper
import FlaskServer.converters as converters
import os, sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def recent_events_route(req):
    if req.method == 'GET':
        attributes_list = []
        try:
            top = None
            if 'top' in req.args:
                top = req.args['top']

            # Load mapping JSON file
            data = load_mapping_json_file(os.path.join(__location__, 'recent-events.json'))

            # Get last event number
            attributes_list.append(attributeshelper.LAST_EVENTS_NUMBER)
            
            attributes_list.append(attributeshelper.SYS_UP_TIME)

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)
            
            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            # Get number of events to build matching json
            number_of_events = ubus_attributes_dict[attributeshelper.LAST_EVENTS_NUMBER[ubuscontroller.NAME_KEY]]

            if int(number_of_events) > 256:
                number_of_events = 256

            time_after_boot = ubus_attributes_dict[attributeshelper.SYS_UP_TIME[ubuscontroller.NAME_KEY]]

            if top:
                number_of_events = top

            if not number_of_events:
                response_json = wrap_data([])
                return response_json

            if not time_after_boot:
                response_json = wrap_data([])
                return response_json

            sys_up_time = getSysUpTime(time_after_boot)

            # Add rows to table and update proper index
            inflate_table(data, int(number_of_events))

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(data))

            success = bool(ubus_attributes_dict)

            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            # Convert values in dictionary
            # Need to parse interface name
            for key, val in ubus_attributes_dict.iteritems():
                if 'severity' in key and ubus_attributes_dict[key] and ubus_attributes_dict[key] != '0':
                    ubus_attributes_dict[key] = converters.EVENTS_SEVERITY[val]
                if 'interfaceName' in key and ubus_attributes_dict[key]:
                    ubus_attributes_dict[key] = getInterfaceName(ubus_attributes_dict[key])
                if 'dateAndTime' in key and ubus_attributes_dict[key]:
                    ubus_attributes_dict[key] = getConvertedTimeFromTimeT(ubus_attributes_dict[key], sys_up_time)

            # Copy received data to original dictionary
            match_json(data, ubus_attributes_dict)

            # Wrap data
            response_json = wrap_data(data)

            return response_json

        except:
            radlogger.log('recent_events_route', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json
