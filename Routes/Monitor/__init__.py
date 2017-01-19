from FlaskServer.jsonutils import *
from FlaskServer.utils import *
from FlaskServer import radlogger
from FlaskServer.Resources import en as resource
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.converters as converters
import os, sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def monitor_route(req):
    if req.method == 'GET':
        attributes_list = []

        try:
            # Load mapping JSON file
            data = load_mapping_json_file(os.path.join(__location__, 'monitor.json'))

            inflate_table(data['configMonitor']['wifiRssiTable'], 5)

            # Sent list to ubus
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(data))
            
            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json
            
            # Convert values in dict
            if 'hsuLinkState' in ubus_attributes_dict and ubus_attributes_dict['hsuLinkState']:
                ubus_attributes_dict['hsuLinkState'] = converters.HSU_LINK_STATE[ubus_attributes_dict['hsuLinkState']]

            if 'hsuAirState' in ubus_attributes_dict and ubus_attributes_dict['hsuAirState']:
                ubus_attributes_dict['hsuAirState'] = converters.HSU_AIR_STATE[ubus_attributes_dict['hsuAirState']]

            if 'hsuTput' in ubus_attributes_dict and ubus_attributes_dict['hsuTput']:
                ubus_attributes_dict['hsuTput'] = compresseddatahelper.calc_current_eth_tput(ubus_attributes_dict['hsuTput'])

            if 'realTimeAndDate' in ubus_attributes_dict and ubus_attributes_dict['realTimeAndDate']:
                ubus_attributes_dict['realTimeAndDate'] = compresseddatahelper.convert_oct_to_date(ubus_attributes_dict['realTimeAndDate'])

            # Config monitor values
            cast_to_int(ubus_attributes_dict,'maxEirp', 'totalTxPower')
            if 'wifiApStatus' in ubus_attributes_dict and ubus_attributes_dict['wifiApStatus']:
                ubus_attributes_dict['wifiApStatus'] = converters.WIFI_AP_STATUS[ubus_attributes_dict['wifiApStatus']]

            # Active Alarms Counter
            if 'activeAlarmsCounter' in ubus_attributes_dict:
                ubus_attributes_dict['activeAlarmsCounter'] = parse_active_alarms_counter(ubus_attributes_dict['activeAlarmsCounter'])

            # Build response
            match_json(data, ubus_attributes_dict)

            parse_wifi_rssi_table(data['configMonitor'])

            parsed_data = compresseddatahelper.parse_hsu_monitor(data['hsuCompressedMonitor'])
            if parsed_data:
                for val in parsed_data:
                    data[val] = parsed_data[val]

            data['installConfirmRequired'] = parsed_data['installConfirmRequired'] and parsed_data['installConfirmRequired'] == resource.unregistered
            
            parsed_data = compresseddatahelper.parse_hbs_monitor(data['hbsCompressedMonitor'])
            if parsed_data:
                for val in parsed_data:
                    data[val] = parsed_data[val]

            # Sanitize data
            data.pop('hsuCompressedMonitor', None)
            data.pop('hbsCompressedMonitor', None)

            # Wrap data
            response_json = wrap_data(data)
            return response_json

        except:
            radlogger.log('monitor_route GET method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

def parse_wifi_rssi_table(raw_data):
    try:
        if raw_data['wifiRssiTable']:
            for idx, val  in enumerate(raw_data['wifiRssiTable']):
                if val['rssiAndMac']:
                    macAndRss = str(val['rssiAndMac'])
                    mac = macAndRss.split(',')[0]
                    rssi = macAndRss.split(',')[1]
                    raw_data['wifiRssiTable'][idx]['mac'] = mac
                    raw_data['wifiRssiTable'][idx]['rssi'] = rssi
    
                raw_data['wifiRssiTable'][idx].pop('rssiAndMac', None)
    except:
        radlogger.log('parse_wifi_rssi_table', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def parse_active_alarms_counter(indexes):
    if not indexes or indexes == 'none' or indexes == 'None':
        return 0
    return len(indexes.split(','))