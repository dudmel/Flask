import datetime, time
import glob
import os
import consts as consts 

TRUE = 1
FALSE = 0

# Delete all cache and .pyc files
def clean():
    filelist = glob.glob("*.cache")
    for f in filelist:
        os.remove(f)  # delete all cache files

# Wrap response data in 'data' key. 
def wrap_data(data, msg=None, error=None):
    response_object = {}
    response_object['data'] = data
    if msg:
        response_object['data']['message'] = msg
    if error:
        response_object['error'] = {}
        response_object['error']['message'] = error
    return response_object

def get_date_string(date_time, reboot_time):

    date = datetime.now() + timedelta(seconds=date_time)

    newDate = reboot_time + timedelta(milliseconds=date_time)

    return newDate

def cast_to_int(dict, *keys):
    for key in keys: 
        if key in dict and dict[key]:
            dict[key] = int(dict[key])

def cast_to_int_divide_by_factor(dict, factor, *keys):
    for key in keys: 
        if key in dict and dict[key] and factor:
            dict[key] = int(dict[key]) / factor

def cast_to_int_multiply_by_factor(dict, factor, *keys):
    for key in keys: 
        if key in dict and dict[key] and factor:
            dict[key] = int(dict[key]) * factor


def getInterfaceName(number):
    if number.isdigit() and number == '1':
        return 'Management Port on ODU'
    elif number.isdigit() and number == '101':
        return 'Radio Interface'
    else:
        return ''

def formatFrequency(freq):
    try:

        floatFreq = float(freq)
        result = "{0:0000.00} [MHz]".format(floatFreq / 1000) if floatFreq > 1000000 else '{:.3f} [GHz]'.format(floatFreq / 1000)
        return result
    except:
        return None

def getConvertedTimeFromTimeT(number_of_ticks, rebootTime):

    number_of_seconds = int(number_of_ticks)
    init1970 = datetime.datetime(1970, 1, 1)
    initial2005Date = datetime.datetime(2005, 9, 1)

    date = init1970 + datetime.timedelta(seconds = number_of_seconds)

    rebootTimeWithOneDay = rebootTime - datetime.timedelta(days=1)
    
    if date < rebootTimeWithOneDay:
        #New date = Event time - "9/1/2005 12:00:00" + reboot time
        newDate = rebootTime + (date - initial2005Date)
        #If future time or time before reboot, do not return new date
        if (newDate > datetime.datetime.now() or newDate < (datetime.datetime.now() - datetime.timedelta(days = 1))):
            # DEBUG
            return newDate.strftime(consts.DATE_TIME_FORMAT)
            #return '';
        return newDate.strftime(consts.DATE_TIME_FORMAT)
    return date.strftime(consts.DATE_TIME_FORMAT)

def getSysUpTime(number_of_ticks):
    number_of_seconds = int(number_of_ticks)/100
    return_time = datetime.datetime.now() - datetime.timedelta(seconds = number_of_seconds)
    return return_time

def getFetureSupportByCapability(capabilityBitmask, index):
    capabilities = list(capabilityBitmask)
    if (len(capabilities) < (index - 1)):
        return false

    intIndex = int(index)
    return capabilities[index] != '0'

def get_base_dir():
    return os.path.abspath(os.path.dirname(__file__))

