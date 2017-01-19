from FlaskServer import app
from subprocess import Popen, PIPE
from FlaskServer.utils import *
import json
import os, sys
import urllib2
from FlaskServer import radlogger

if os.name == 'posix' and app.config['USE_UBUS_C']:
    import ubus as ubus
    ubus.InitializeUBusClient("management")

if os.name == 'nt':
    import requests

#enum eRequestStatus
#{
#               // SNMP Error Statuses
#               E_MNG_REQ_STATUS_NO_ERR = 0
#               E_MNG_REQ_STATUS_TOO_BIG ,
#               E_MNG_REQ_STATUS_NO_SUCH_NAME,
#               E_MNG_REQ_STATUS_BAD_VALUE,
#               E_MNG_REQ_STATUS_READ_ONLY,
#               E_MNG_REQ_STATUS_GEN_ERR,
#               E_MNG_REQ_STATUS_MAX
#};

GET_ACTION = 0
SET_ACTION = 1
LOCAL_DESTINATION = 'local'
REMOTE_DESTINATION = 'remote'
UBUS_SHELL_COMMAND = 'ubus call management web '
UBUS_PATH = 'management'
UBUS_METHOD = 'web'
__TRANSACTION__ = 'transaction'
__ACTION__ = 'action'
__DESTINATION__ = 'destination'
__VALUE__ = 'value'
__NAME__ = 'name'
__INDEX__ = 'index'
__ATTR__ = 'attr'
__OBJECT__ = 'object'
__STATUSCODE__ = 'statusCode'

# Getters
NAME_KEY = __NAME__
VALUE_KEY = __VALUE__
OBJECT_KEY = __OBJECT__
ATTR_KEY = __ATTR__
INDEX_KEY = __INDEX__

#Dev
perl_file_path = '//multi-server/Software/Perl/Perl_5.8/bin/perl.exe P:/HighLink/Groups/Software/NMS/Perl/ULC/bulkTelnetAttrRequestHsu.pl '

# Get attributes from ODU using ubus
def get_attributes_ubus(attributes):
    
    if not attributes:
        return "" 
    
    _attributes = attributes
    
    if isinstance(attributes, dict):
        _attributes = []
        _attributes.append(attributes)

    return call_ubus_transaction(GET_ACTION, _attributes)

# Set attributes from ODU using ubus
def set_attributes_ubus(attributes):
    
    if not attributes:
        return "" 

    _attributes = attributes
    
    if isinstance(attributes, dict):
        _attributes = []
        _attributes.append(attributes)

    return call_ubus_transaction(SET_ACTION, _attributes)

def call_ubus_transaction(action, attributes):
   
    if os.name == 'nt': #Windows
        #return windows_perl_interface_dev_only(action, attributes)
        return windows_http_interface_debug(action, attributes)
    elif os.name == 'posix': # Linux ULC
        if app.config['USE_UBUS_C']:
            return linux_ubusc_interface(action, attributes)
        else:
            return linux_ubus_interface(action, attributes)

def linux_ubus_interface(action, attributes):

    try:

        # Build json to be sent via ubus management call
        ubus_call = {}
        ubus_call[__ACTION__] = action
        ubus_call[__DESTINATION__] = LOCAL_DESTINATION
        ubus_call[__TRANSACTION__] = []
        for attr in attributes:
            if VALUE_KEY in attr:
                attr[__VALUE__] = str(attr[__VALUE__]).encode('utf-8')
            ubus_call[__TRANSACTION__].append(attr)

        comm = UBUS_SHELL_COMMAND + "'{0}'".format(str(ubus_call).replace("'","\""))

        try:
            ubus = Popen(comm, shell=True,
                stdout = PIPE,
                stderr = PIPE)
            ubus_response, error = ubus.communicate()
            ubus_json_response = json.loads(ubus_response)
            #if "hsuCompressedMonitor" not in ubus_response:
            #    print ubus_response + "\n"
        except:
            radlogger.log('linux_ubus_interface POST method.', sys.exc_info())
            return None
    
        if not ubus_json_response:
            return None

        pretify_ubus_call = {}

        for attr in ubus_json_response[__TRANSACTION__]:
            if attr.has_key(__STATUSCODE__):
                if int(attr[__STATUSCODE__]) != 0 and action == SET_ACTION:
                    print 'ERROR: ' + attr[__NAME__] + ' have error code ' + str(attr[__STATUSCODE__]) + ' !!!'
                    return None
        
            pretify_ubus_call[attr[__NAME__]] = attr[__VALUE__]

        return pretify_ubus_call
    except:
        print('Unexpected error in OLD linux_ubus_interface:', sys.exc_info()[0])
        return None

# UBUS C API (ubus.py)
def linux_ubusc_interface(action, attributes):
    try:
        ubus_call = {}

        # Build json to be sent via ubus management call
        ubus_call[__ACTION__] = action
        ubus_call[__DESTINATION__] = LOCAL_DESTINATION
        ubus_call[__TRANSACTION__] = []

        for attr in attributes:
            if VALUE_KEY in attr:
                attr[__VALUE__] = str(attr[__VALUE__]).encode('utf-8')
            ubus_call[__TRANSACTION__].append(attr)

        comm ="{0}".format(str(ubus_call).replace("'","\""))
        try:
            ubus_response = ubus.SendJsonRequest(UBUS_METHOD, comm, 1)
        except:
            radlogger.log('Unexpected error in linux_ubus_interface SEND ACTION:', sys.exc_info())
            return None
    
        if app.config['PRINT_ALL']:
            radlogger.log(ubus_response + '\n\n', None)
        elif app.config['PRINT_RESPONSES'] and 'hsuLinkState' not in str(ubus_response) and 'realTimeAndDate' not in str(ubus_response):
            radlogger.log(ubus_response + '\n\n', None)

        if (ubus_response):
            ubus_json_response = json.loads(ubus_response)

        if not ubus_json_response:
            return None

        pretify_ubus_call = {}
        for attr in ubus_json_response[__TRANSACTION__]:
            if attr.has_key(__STATUSCODE__):
                if int(attr[__STATUSCODE__]) != 0 and action == SET_ACTION:
                    radlogger.log('ERROR: ' + attr[__NAME__] + ' have error code ' + str(attr[__STATUSCODE__]) + ' !!!', None)
                    return None
        
            
            pretify_ubus_call[attr[__NAME__]] = attr[__VALUE__]

        return pretify_ubus_call
    except:
        radlogger.log('GLOBAL Unexpected error in linux_ubus_interface:', sys.exc_info())
        return None

def windows_perl_interface_dev_only(action, attributes):

    if action == GET_ACTION:
        action_debug = 'GET'
    elif action == SET_ACTION:
        action_debug = 'SET'

    full_path = perl_file_path + " " + action_debug + " "

    for obj in attributes:
        if action == GET_ACTION:
            full_path += str(obj[__OBJECT__]) + ',' + str(obj[__ATTR__]) + "," + str(obj[__INDEX__]) + " "
        elif action == SET_ACTION:
            full_path += str(obj[__OBJECT__]) + ',' + str(obj[__ATTR__]) + "," + str(obj[__INDEX__]) + "," + str(obj[__VALUE__]) + " "

    numcomms = Popen(full_path, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    out, err = numcomms.communicate()
    
    print 'Error:\n'
    print err
    print "\n Response: \n"
    print out
    
    res = out.strip().split('#')

    pretify_ubus_call = {}

    for idx, attr in enumerate(attributes):
        pretify_ubus_call[attr[__NAME__]] = res[idx]
    
    return pretify_ubus_call

def windows_http_interface_debug(action, attributes):

    if action == GET_ACTION:
        action_debug = 'GET'
    elif action == SET_ACTION:
        action_debug = 'SET'

    resp_data = ''
    ip = '10.103.77.60'
    url = 'http://' + ip +'/api/v1/debug/attribute?'

    try:

        for obj in attributes:
            if action == GET_ACTION:
                url_params = 'object=' + str(obj[__OBJECT__]) + '&attr=' + str(obj[__ATTR__]) + "&index=" + str(obj[__INDEX__])
                #print url + url_params
                response = requests.get(url + url_params)
            elif action == SET_ACTION:
                url_params = 'object=' + str(obj[__OBJECT__]) + '&attr=' + str(obj[__ATTR__]) + "&index=" + str(obj[__INDEX__]) + "&value=" + str(obj[__VALUE__])
                #print "\n POST: " + url + '' + url_params
                response = requests.post(url + url_params)

            data = None
            try:
                data = json.loads(response.text)
            except:
                radlogger.log('Error in windows_http_interface_debug: ' + response.text , sys.exc_info())
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            success = bool(data)

            if (not data['data'] and 'message' in data['error']):
                print data['error']['message']
                return None

            if not success:
                radlogger.log('windows_http_interface_debug response is empty', None)
                return None
            
            resp_data += data['data'] + '#'

        resp_data = resp_data[:-1]

        try:
            res = resp_data.strip().split('#')

            pretify_ubus_call = {}

            for idx, attr in enumerate(attributes):
                #print idx
                #print attr[__NAME__]
                pretify_ubus_call[attr[__NAME__]] = res[idx]

            return pretify_ubus_call
        except:
            radlogger.log("ERROR windows_http_interface_debug::split data failed" , sys.exc_info())
            return None
    except:
        radlogger.log("ERROR windows_http_interface_debug::general error" , sys.exc_info())
        return None    