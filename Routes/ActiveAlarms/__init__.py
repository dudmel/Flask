from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.attributeshelper as attributeshelper
import FlaskServer.converters as converters
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def active_alarms_route(req):
    if req.method == 'GET':
        attributes_list = []
        try:
            response_json = wrap_data([])

            # Load mapping JSON file
            data = load_mapping_json_file(os.path.join(__location__, 'active-alarms.json'))

            # Get active alarms indexes
            attributes_list.append(attributeshelper.ACTIVE_ALARMS_INDEXES)
            attributes_list.append( attributeshelper.SYS_UP_TIME)

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)
            
            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            # Get number of active alarms to build matching json
            indexes_of_alarms = ubus_attributes_dict[attributeshelper.ACTIVE_ALARMS_INDEXES[ubuscontroller.NAME_KEY]]
            indexes_of_alarms = indexes_of_alarms.replace(" ", "")
            time_after_boot = ubus_attributes_dict[attributeshelper.SYS_UP_TIME[ubuscontroller.NAME_KEY]]

            if not bool(indexes_of_alarms):
                response_json = wrap_data([])
                return response_json

            if (indexes_of_alarms == '' or indexes_of_alarms == 'none' or indexes_of_alarms == 'None'):
                response_json = wrap_data([])
                return response_json

            if not bool(time_after_boot):
                response_json = wrap_data([])
                return response_json

            sys_up_time = getSysUpTime(time_after_boot)

            indexesList = indexes_of_alarms.split(',')

            # DEBUG TEST Generate multiple alarms // Remove before flight!
            #if len(indexesList) == 1:
            #     indexesList.append(indexesList[0])

            # Add rows to table and update proper index
            inflate_table_for_indexesList(data, indexesList)

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(data))
                        
            if not bool(ubus_attributes_dict):
                response_json = wrap_data([])
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
            radlogger.log('trapsdestinations_route POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json