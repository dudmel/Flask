from werkzeug import secure_filename
from FlaskServer import app, radlogger
from FlaskServer.jsonutils import *
from FlaskServer.utils import *
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.compresseddatahelper as compresseddatahelper
import FlaskServer.attributeshelper as attributeshelper
import FlaskServer.converters as converters
import copy, os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def spectrum_range(req):
    try:
       
        # Return Chip Min Max Frequencies
        attributes_list = [attributeshelper.AIR_CHIP_MIN_MAX_FREQ,
                           attributeshelper.AIR_MIN_FREQ,
                           attributeshelper.AIR_MAX_FREQ]

        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)
        min_max_freq = ubus_attributes_dict[attributeshelper.AIR_CHIP_MIN_MAX_FREQ[ubuscontroller.NAME_KEY]]
        air_min_freq = ubus_attributes_dict[attributeshelper.AIR_MIN_FREQ[ubuscontroller.NAME_KEY]]
        air_max_freq = ubus_attributes_dict[attributeshelper.AIR_MAX_FREQ[ubuscontroller.NAME_KEY]]

        if min_max_freq:
            min_chip = min_max_freq.split('|')[0]
            max_chip = min_max_freq.split('|')[1]
           
        data = {}
        data['minChipFrequency'] = int(min_chip)
        data['maxChipFrequency'] = int(max_chip)
        data['minAirFrequency'] = int(air_min_freq)
        data['maxAirFrequency'] = int(air_max_freq)
        
        response_json = wrap_data(data)
        
        return response_json

    except:
        radlogger.log('spectrum_range', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def spectrum_table(req):
    try:
        attributes_list = []
        
        # Load mapping JSON file
        data = load_mapping_json_file(os.path.join(__location__, 'spectrum.json'))

        # Get spectrum channels number
        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributeshelper.NUMBER_OF_SPECTRUM_CHANNELS)           
            
        if not bool(ubus_attributes_dict):
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        number_of_channels = ubus_attributes_dict[attributeshelper.NUMBER_OF_SPECTRUM_CHANNELS[ubuscontroller.NAME_KEY]]

        if not number_of_channels:
            return

        # Add rows to table and update proper index
        inflate_table(data, int(number_of_channels))

        # Sent list to ubus
        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(data))

        if not bool(ubus_attributes_dict):
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        # Convert values in dict
        for key, val in ubus_attributes_dict.iteritems():
            if 'spectrumChannelScanned' in key and ubus_attributes_dict[key] and ubus_attributes_dict[key] != '0':
                ubus_attributes_dict[key] = converters.SPECTRUM_CHANNEL_SCANNED[val]

        # Copy received data to original dictionary
        match_json(data, ubus_attributes_dict)

        inverted_data = {}
        inverted_data['spectrumChannelFrequncy'] = []
        inverted_data['currentAntennaA'] = []
        inverted_data['currentAntennaB'] = []
        inverted_data['averageAntennaA'] = []
        inverted_data['averageAntennaB'] = []
        inverted_data['maxAntennaA'] = []
        inverted_data['maxAntennaB'] = []
        for row in data:
            if row['spectrumChannelScanned'] == 'Scanned':
                inverted_data['spectrumChannelFrequncy'].append(row['spectrumChannelFrequncy'])
                inverted_data['currentAntennaA'].append(int(row['currentAntennaA']))
                inverted_data['currentAntennaB'].append(int(row['currentAntennaB']))
                inverted_data['averageAntennaA'].append(int(row['averageAntennaA']))
                inverted_data['averageAntennaB'].append(int(row['averageAntennaB']))
                inverted_data['maxAntennaA'].append(int(row['maxAntennaA']))
                inverted_data['maxAntennaB'].append(int(row['maxAntennaB']))

        # Wrap data
        response_json = wrap_data(inverted_data)

        return response_json

    except:
        radlogger.log('spectrum_table', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def start_spectrum(req):
    try:
        min_freq = None
        max_freq = None
        duration = None

        if 'min' in req.args:
            min_freq = req.args['min']
        
        if 'max' in req.args:
            max_freq = req.args['max']
        
        if 'duration' in req.args:
            duration = req.args['duration']

        if not min_freq or not max_freq or not duration:
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        start_command =  copy.deepcopy(attributeshelper.START_SPECTRUM)
        start_command['value'] = '{0},{1},{2},{3}'.format(start_command['value'], min_freq, max_freq, duration)

        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(start_command)
        
        if not bool(ubus_attributes_dict):
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        response_json = wrap_data({}, "Spectrum measurement started")

        return response_json
    
    except:
        radlogger.log('start_spectrum', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def stop_spectrum(req):
    try:

        stop_command =  copy.deepcopy(attributeshelper.STOP_SPECTRUM)
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(stop_command)

        response_json = wrap_data({}, "Spectrum measurement stopped")
        return response_json
    
    except:
        radlogger.log('stop_spectrum', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json