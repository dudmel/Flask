import ipaddress, random, sys, datetime
from FlaskServer import radlogger, converters
from FlaskServer.utils import *

BITS_NUM_IN_BITS = 1000000.0
BITS_NUM_IN_KBITS = 1000.0

def parse_hsu_static(raw_value):
    names = ['hbsLocation', 'hbsIp', 'hbsSubnetMask', 'hbsAntennaType', 'hbsAgentVersion', 'hbsName']

    if not raw_value:
        return None

    result = {}
    splitted = str(raw_value).split(',')
    if not splitted or len(splitted) != 6:
        return result

    # Example data: London,0A674D64,FFFFFF00,4,3155,SuperName
    for idx, name in enumerate(names):
        result[name] = splitted[idx]

    try:
        # Convert hex -> decimal -> ip
        result[names[1]] = str(ipaddress.IPv4Address(int(result[names[1]], 16)))
    except:
        radlogger.log('parse_hsu_static method.', sys.exc_info())
        return None

    try:
        # Convert hex -> decimal -> subnet mask
        result[names[2]] = str(ipaddress.IPv4Address(int(result[names[2]], 16)))
    except:
        radlogger.log('parse_hsu_static method.', sys.exc_info())
        return None

    return result

def parse_hsu_monitor(raw_value):
    if not raw_value:
        return None

    try:
    
        # Split string to list of integers
        if '|' in raw_value:
            splitted = raw_value.strip('|').split('|')
        else:
            splitted = raw_value.split()

        byte_array = [int(i) for i in splitted if i != '']
    
        lan1_rx_bytes = [byte_array[16], byte_array[17], byte_array[18], byte_array[19]]
        lan1_tx_bytes = [byte_array[20], byte_array[21], byte_array[22], byte_array[23]]
        lan1_rx_frames = [byte_array[24], byte_array[25], byte_array[26], byte_array[27]]
        lan1_tx_frames = [byte_array[28], byte_array[29], byte_array[30], byte_array[31]]

        atpcStateDict = parceAtpcData(byte_array[50]);
        installConfirmReq = 'True' if byte_array[51] == '1' else "False";

        parsed_list = [convert_kbps_to_mbps(lan1_rx_bytes), 
                convert_kbps_to_mbps(lan1_tx_bytes),
                convert_to_frames(lan1_rx_frames),
                convert_to_frames(lan1_tx_frames)]

        result = {}
        result['hsuLan1RxMbps'] = parsed_list[0]; 
        result['hsuLan1TxMbps'] = parsed_list[1]; 
        result['hsuLan1RxFps'] = parsed_list[2]; 
        result['hsuLan1TxFps'] = parsed_list[3]; 

        result['installConfirmRequired'] = installConfirmReq;
    
        allKeys = atpcStateDict.keys()
        for key in allKeys:
            result[key] = atpcStateDict[key]

        return result
    except:
        radlogger.log('parse_hsu_monitor method.', sys.exc_info())
        return None

def parse_hbs_monitor(raw_value):
    try:
        if not raw_value:
            return None

        names = ["hbsRss", "hbsTput", "hbsLan1RxMbps", "hbsLan1TxMbps"]

        # Split string to list of integers
        if '|' in raw_value:
            splitted = raw_value.split('|')
        else:
            splitted = raw_value.split()

        byteArray = [int(i) for i in splitted if i != '']

        hbs_rss =  byteArray[0] - 255                
        hbs_tput = [byteArray[2], byteArray[3], byteArray[4], byteArray[5]]
        hbs_lan1_rx_bytes = [byteArray[63], byteArray[64], byteArray[65], byteArray[66]]
        hbs_lan1_tx_bytes = [byteArray[67], byteArray[68], byteArray[69], byteArray[70]]  
        
        parsed_list = [hbs_rss,
                       convert_hex_to_bps(hbs_tput),
                       convert_kbps_to_mbps(hbs_lan1_rx_bytes),
                       convert_kbps_to_mbps(hbs_lan1_tx_bytes)]

        result = {}

        for idx, name in enumerate(names):
            result[name] = parsed_list[idx]

        return result
    except:
        radlogger.log('parse_hbs_monitor method.', sys.exc_info())
        return None   

def parceAtpcData(number):

    atpcDict = {};
    atpcDict['atpcSupported'] = '';
    atpcDict['atpcStstus'] = converters.ATPC_STATUSES['0'];
    atpcDict['atpcRequiredRateAchieved'] = '';
    atpcDict['atpcNumberOfLoweredDbs'] = '';

    try:
        stringInBits = bin(number);
        bitmask = stringInBits[2:];

        atpcDict['atpcSupported'] = 'True' if bitmask[0:1] == '1' else 'False'
        if atpcDict['atpcSupported'] == 'True':
            status = int(bitmask[1:2], 2)
            requiredRateAchieved = bitmask[3:4]
            numberOfLoweredDbs = int(bitmask[4:], 2)

            atpcDict['atpcStstus'] = converters.ATPC_STATUSES[str(status)];
            atpcDict['atpcRequiredRateAchieved'] = 'True' if requiredRateAchieved == '1' else 'False';
            atpcDict['atpcNumberOfLoweredDbs'] = numberOfLoweredDbs;
            return atpcDict;
    except:
        radlogger.log('parceAtpcData method.', sys.exc_info())
        return atpcDict;

def parse_spectrum_compressed(raw_value):
    names = ["frequency", "scanned", "timestamp", 
             "lastNFAntennaA", "lastNFAntennaB", 
             "avgNFAntennaA", "avgNFAntennaB",
             "maxNFAntennaA", "maxNFAntennaB",
             "cacPerformed", "lastCACTimestamp",
             "radarDetected", "radarDetectedTimestamp",
             "channelAvailable", "maxBeaconRSS"]

    if not raw_value:
        return None
    
    # Split string to list of integers
    if '|' in raw_value:
        splitted = raw_value.strip('|').split('|')
    else:
        splitted = raw_value.split()

def convert_kbps_to_mbps(byte_array):
   
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    to_mbps = round(to_int / BITS_NUM_IN_KBITS, 1)

    return to_mbps

def convert_bps_to_mbps(byte_array):
   
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    to_mbps = round(to_int / BITS_NUM_IN_BITS, 1)

    return to_mbps

def convert_hex_to_bps(byte_array):
   
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    return to_int

def convert_to_frames(byte_array):
    
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    return to_int

def convert_hex_to_int(byte_array):
    
    in_hex = ''.join('{:02x}'.format(x) for x in byte_array)

    to_int = int(in_hex, 16)

    return to_int

def calc_current_eth_tput(raw_value):
    
    value = int(raw_value)
    return value
    #if value == -1:
    #    return -1
    #if value >= 0:
    #    return round(value / BITS_NUM_IN_BITS, 1 if value > BITS_NUM_IN_BITS else 2)

def parse_speed_test(raw_value):
    try:
        if not raw_value:
            return None

        names = ["dlSpeed", "ulSpeed"]

        # Split string to list of integers
        if '|' in raw_value:
            splitted = raw_value.split('|')
        else:
            splitted = raw_value.split()

        byteArray = [int(i) for i in splitted if i != '']

        download_speed = [byteArray[96], byteArray[97], byteArray[98], byteArray[99]] 
        upload_speed = [byteArray[100], byteArray[101], byteArray[102], byteArray[103]] 
        
        parsed_list = [convert_bps_to_mbps(download_speed),
                       convert_bps_to_mbps(upload_speed)]

        result = {}

        for idx, name in enumerate(names):
            result[name] = parsed_list[idx]

        return result
    except:
        print('Unexpected error:', sys.exc_info()[0])
        return 0

def convert_oct_to_date(raw_value):
    try:
        if not raw_value:
            return None

        if '|' in raw_value:
            splitted = raw_value.split('|')
        else:
            splitted = raw_value.split()
        
        byteArray = [int(i) for i in splitted if i != '']

        hex1 = ''.join('{:02x}'.format(byteArray[0]))
        hex2 = ''.join('{:02x}'.format(byteArray[1]))
        year = int(hex1 + hex2, 16)
        month = byteArray[2]
        day = byteArray[3]
        hour = byteArray[4]
        min = byteArray[5]
        sec = byteArray[6]

        date = datetime.datetime(year,month, day, hour, min, sec)
        return date.isoformat()
    except:
        radlogger.log('convert_oct_to_date.', sys.exc_info())
        return 0

