import FlaskServer.Authentication as Auth
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.attributeshelper as attributeshelper
from FlaskServer import app
from threading import Timer
from FlaskServer.Routes.Monitor import monitor_route
from FlaskServer import radlogger
from FlaskServer.Routes.System import system_route
from FlaskServer.Routes.Network import network_route
from FlaskServer.Routes.Wifi import wifi_route
from FlaskServer.Routes.Radio import radio_route
from FlaskServer.Routes.RecentEvents import recent_events_route
from FlaskServer.Routes.TrapsDestinations import trapsdestinations_route
import FlaskServer.compresseddatahelper as compresseddatahelper
from FlaskServer.utils import *
from flask import send_file
import subprocess, os, sys, random, json, ipaddress

RESET_TIMER = 3

RESTORE_TO_DEFAULTS_WITH_DEFAULT_IP_ADDRESS_VALUE = 1
RESTORE_TO_DEFAULTS_KEEP_EXISTING_IP_ADDRESS_VALUE = 2

INVALID_IP_ADDRESS = 'Invalid IP address'
INVALID_PACKET_COUNT = 'Invalid packet count'
INVALID_PACKET_SIZE = 'Invalid packet size'
LACK_OF_ARGUMENTS = "Lack of arguments passed"

def speed_test(action, req):
    if req.method == 'GET' and action == 'data':
        try:       
            attributes_list = []

            attributes_list = [attributeshelper.HBS_COMPRESSED_MONITOR]

            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            parsed_data = compresseddatahelper.parse_speed_test(ubus_attributes_dict[attributeshelper.HBS_COMPRESSED_MONITOR['name']])

            response = {}
            response['ulSpeed'] = parsed_data['ulSpeed']
            response['dlSpeed'] = parsed_data['dlSpeed']
            
            response_json = wrap_data(response)
            return response_json
        except:
            radlogger.log('speed_test GET method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

    if req.method == 'POST':
        try:

            if action == 'start':
                # Start speed test, every 30 seconds (client side)
                command = attributeshelper.START_SPEED_TEST
                ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)
                response_json = wrap_data({}, "Speed Test Initiated")
                return response_json

            elif action == 'stop':
                # Parameter to enable Evaluation process (1-On, 2-Off)
                command = attributeshelper.STOP_SPEED_TEST
                ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)
                response_json = wrap_data({}, "Speed Test Stopped")
                return response_json
            else:
                response_json = wrap_data({}, error="Invalid command")
                return response_json
        except:
            radlogger.log('speed_test POST method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

def deregister_local_route(req):

    try:
        command = attributeshelper.DEREGISTER_COMMAND
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)

        if (not ubus_attributes_dict):
            response_json = wrap_data({}, error="Unable to set value")
            return response_json
        
        response_json = wrap_data({}, "Done")
        return response_json

    except:
        radlogger.log('deregister_device_route', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def ping(req):
    try:
        min_packet_size = 0
        max_packet_size = 1472

        min_packet_count = 1
        max_packet_count = 30

        request = req.get_json()

        if not 'ip' in request or not 'packetCount' in request or not 'packetSize' in request:
            response_json = wrap_data({}, error = LACK_OF_ARGUMENTS)
            return response_json

        ip = request['ip']
        packetCount = str(request['packetCount'])
        packetSize = str(request['packetSize'])

        import ipaddress
        try:
            ipaddress.ip_address(ip)
        except:
            response_json = wrap_data({}, error = INVALID_IP_ADDRESS)
            return response_json

        if not packetCount.isdigit() or int(packetCount) < min_packet_count or int(packetCount) > max_packet_count:
            response_json = wrap_data({}, error = INVALID_PACKET_COUNT)
            return response_json

        if not packetSize.isdigit() or int(packetSize) < min_packet_size or int(packetSize) > max_packet_size:
            response_json = wrap_data({}, error = INVALID_PACKET_SIZE)
            return response_json

        if os.name == 'nt': #Windows
            count = '-n'
            size = '-l'
        elif os.name == 'posix': # Linux ULC
            count = '-c'
            size = '-s'

        ping = subprocess.Popen(["ping", count, packetCount, size, packetSize, ip],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
        
        out, error = ping.communicate()
        
        response = {}
        response['result'] = out
        
        response_json = wrap_data(response)
        return response_json

    except:
        radlogger.log('ping method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def trace(req):
    try:

        request = req.get_json()
        if not 'ip' in request:
            response_json = wrap_data({}, error = LACK_OF_ARGUMENTS)
            return response_json

        ip = request['ip']

        import ipaddress
        try:
            ipaddress.ip_address(ip)
        except:
            response_json = wrap_data({}, error = INVALID_IP_ADDRESS)
            return response_json
        
        if os.name == 'nt': #Windows
            trace = subprocess.Popen(['tracert', ip],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
            out, error = trace.communicate()
        elif os.name == 'posix': # Linux ULC
            trace = subprocess.Popen(['traceroute', '-m', '5', ip],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
            out, error = trace.communicate()

        response = {}
        response['result'] = out
        
        response_json = wrap_data(response)
        return response_json

    except:
        radlogger.log('trace method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def linux_reset():
    try:
       
        reboot = subprocess.Popen(["reboot"],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
        out, error = trace.communicate()
        
    except:
        radlogger.log('linux_reset method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def odu_reset():
    try:
       
        command = attributeshelper.RESET_COMMAND
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)

        if (not ubus_attributes_dict):
            response_json = wrap_data({}, error="Unable to set value")
            return response_json
        
        response_json = wrap_data({}, "Done")
        return response_json

    except:
        radlogger.log('odu_reset method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def resync():
    try:
        command = attributeshelper.RESYNC_COMMAND
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)

        response_json = wrap_data({}, "Done")
        return response_json

    except:
        radlogger.log('resync method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def change_link_password(req):
    
    try:
        current_password = req.get_json()['currentPassword']
        new_password = req.get_json()['newPassword']

        if current_password and new_password:
            command = attributeshelper.CHANGE_LINK_PASSWORD

            command['value'] = '{0}.{1}'.format(current_password,new_password)

            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)

            if bool(ubus_attributes_dict):
                response = {}
                response_json = wrap_data({}, "Link Password changed successfully")
                return response_json
            else:
                response_json = wrap_data({}, error="Error occurred")
                return response_json
    except:
        radlogger.log('change_link_password method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def restore_to_defaults(req):
    try:
        is_default_ip_required = req.get_json()['isDefaultIpRequired']

        command = attributeshelper.RESTORE_TO_DEFAULTS
        setValue = RESTORE_TO_DEFAULTS_WITH_DEFAULT_IP_ADDRESS_VALUE if is_default_ip_required else RESTORE_TO_DEFAULTS_KEEP_EXISTING_IP_ADDRESS_VALUE
        command['value'] = setValue

        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)

        success = bool(ubus_attributes_dict)

        if success:
            # Reset ODU on another thread and return response to client
            Timer(RESET_TIMER, odu_reset, ()).start()
            response_json = wrap_data({}, 'Operation performed successfully')
            return response_json
        else: 
            response_json = wrap_data({}, error='Unable to set value')
            return response_json
            
    except:
        radlogger.log('restore_to_defaults method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def get_diagnostics(req):
    try:
        diag_file = os.path.join(app.config['TEMP_FOLDER'], 'diagnostics.json')

        #Get all data
        all_data = {}

        if app.config['TESTING_ROUTES_ENABLED']:
            from FlaskServer.Dev import mockedDataRequest
            # Dev
            all_data['monitor'] = mockedDataRequest(req, 'monitor')['data']
            all_data['network'] = mockedDataRequest(req, 'network')['data']
            all_data['system'] = mockedDataRequest(req, 'system')['data']
            all_data['radio'] = mockedDataRequest(req, 'radio')['data']
            all_data['wifi'] = mockedDataRequest(req, 'wifi')['data']
            all_data['recent-events'] = mockedDataRequest(req, 'recent-events')['data']
            all_data['traps-destinations'] = mockedDataRequest(req, 'traps-destinations')['data']
        else:
            # Prod
            all_data['monitor'] = monitor_route(req)['data']
            all_data['network'] = network_route(req)['data']
            all_data['system'] = system_route(req)['data']
            all_data['radio'] = radio_route(req)['data']
            all_data['wifi'] = wifi_route(req)['data']
            all_data['recent-events'] = recent_events_route(req)['data']
            all_data['traps-destinations'] = trapsdestinations_route(req)['data']

        with open(diag_file, "wb") as outfile:
            json.dump(all_data, outfile, indent=4)

        return send_file(diag_file, mimetype='application/json')

    except:
        radlogger.log('get_diagnostics method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json