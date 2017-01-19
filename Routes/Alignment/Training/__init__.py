from FlaskServer import app
from FlaskServer.utils import *
from FlaskServer.jsonutils import *
from FlaskServer import radlogger
from FlaskServer.Routes.Alignment import *
import FlaskServer.Routes.Alignment.alignmnetmockup as mockup
from threading import Timer
import json, os, math, random

RESET_TIMER = 3

TRAINING_GLOBAL_HASH = {}
TRAINING_GLOBAL_HASH['horizontalStartAngle'] = -175
TRAINING_GLOBAL_HASH['horizontalEndAngle'] = 185
TRAINING_GLOBAL_HASH['horizontalScanStep'] = 10
TRAINING_GLOBAL_HASH['elevationBeamwidth'] = 10
TRAINING_GLOBAL_HASH['tableCellCount'] = 36

TRAINING_INITIAL_DATA = {}
TRAINING_BEST_HBS = {}
TRAINING_MEASURING_SCENARIO = {}
TRAINING_MEASURING_TO_RETURN = {}
TRAINING_FINE_ALIGNMENT = []
TRAINING_EVALUATION_RESULTS = {}

EVALUATION_RESULTS_STACK = []

TRAINING_MODE = '1'
PRODUCTION_MODE = '2'

TRAINING_COMMANDS = {
        'load-scenario': 1, 
        'start': 2, 
        'stop': 3, 
    }

# Action Invoker
def training_action_invoker(req, action):
    if TRAINING_COMMANDS.has_key(action):
        
        if action == 'load-scenario':
            return load_training(req)

        if action == 'start':
            return start_training()

        if action == 'stop':
            return stop_training()

    else:
        response_json = wrap_data({}, error="Invalid command")
        return response_json

# Actions
def load_training(req):
    try:
        training_file = os.path.join(app.config['APP_TEMP_FOLDER'], 'training.json')
        
        #if os.path.isfile(training_file):
        payload = req.get_json()
        
        if not payload:
                response_json = wrap_data({}, error="Unable to load training scenario")
                return response_json
        
        with open(training_file, 'w') as outfile:
            json.dump(payload, outfile, indent=4)
        
        response_json = wrap_data({}, "Training scenario loaded successfully")
        return response_json

    except:
        radlogger.log('load_training method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def start_training():
    try:
        
        switch_to_mode(TRAINING_MODE)

        Timer(RESET_TIMER, linux_reset, ()).start()

        response_json = wrap_data({}, "Switching to Training mode and resetting")
        return response_json

    except:
        radlogger.log('start_training method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def stop_training():

    try:

        switch_to_mode(PRODUCTION_MODE)

        Timer(RESET_TIMER, linux_reset, ()).start()

        response_json = wrap_data({}, "Exiting Training mode and resetting")
        return response_json

    except:
        radlogger.log('stop_training method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

# Routes
def training_alignmentActionInvoker(action, req):
    
    if action == 'start' or action == 'restart':
        init_training_scenario()
    
    # Return generic post for start sync action
    if action == 'startSync':
        return mockup.genericPostResponse()

    # Production !
    return alignmentActionInvoker(action, req)

def training_best_position(req):
    if req.method == 'GET':

        response_json = wrap_data(TRAINING_BEST_HBS)

        return response_json
    
def training_getInitialValues(req):
    if req.method == 'GET':
        response_json = wrap_data(TRAINING_INITIAL_DATA)
        return response_json

def training_fine_alignment(req):
    if req.method == 'GET':
        try:

            # Get real location !!!
            cursorLocation = calculateTrainingCursorLocation()
        
            current_elevation = int(cursorLocation['elevation'])
            current_horizontal = cursorLocation['horizontal']

            fine_response = {}
            fine_response['LinkState'] = 'syncUnregistered'

            # If we hit the best fine alignment rss set equal value
            for fine in TRAINING_FINE_ALIGNMENT:
                if 'FineElevation' in fine and 'FineHorizontal' in fine and fine['FineElevation'] == current_elevation and fine['FineHorizontal'] == current_horizontal:
                    fine_response["RSSUL"] = fine['FineBestRss']
                    fine_response["RSSDL"] = fine['FineBestRss']
                    break
                else:
                # If no hit return higher rss
                    fine_response["RSSUL"] = fine['FineBestRss'] - 1
                    fine_response["RSSDL"] = fine['FineBestRss'] - 1

            response_json = wrap_data(fine_response)

            return response_json
        except:
            radlogger.log('training_fine_alignment method.', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

def training_evaluation_results(req):
    if req.method == 'GET':

        temp_response = copy.copy(TRAINING_EVALUATION_RESULTS)

        temp_response['LinkState'] = 'syncUnregistered'

        if EVALUATION_RESULTS_STACK and EVALUATION_RESULTS_STACK.count > 0:
            val = EVALUATION_RESULTS_STACK.pop()
            temp_response['DownLink'] -= val
            temp_response['UpLink'] -= val
            
        response_json = wrap_data(temp_response)

        return response_json

def training_measuring(req):
    if req.method == 'GET':

        # Get real location !!!
        cursorLocation = calculateTrainingCursorLocation()
        
        if not cursorLocation:
            return None
        
        TRAINING_MEASURING_TO_RETURN['data']['cursorLocation']  = cursorLocation

        # Based on current location modify measuring object
        cell = int(cursorLocation['cellNumber'])
        elevationCell = cursorLocation['elevationCell']
        
        if elevationCell == 'high':
            elevationCell = 'elevationHigh'

        if elevationCell == 'middle':
            elevationCell = 'elevationMedium'

        if elevationCell == 'low':
            elevationCell = 'elevationLow'
        
        # Update return object based on the scenario
        # Mark scanned current elevationCell
        # if we "hit" a HBS mark it on the returned object
        try:
            TRAINING_MEASURING_TO_RETURN['data']['samples'][cell][elevationCell]['scanned'] = 'true'
            
            if TRAINING_MEASURING_SCENARIO['data']['samples'][cell][elevationCell]['scanned'] == 'true':
                TRAINING_MEASURING_TO_RETURN['data']['samples'][cell][elevationCell] = TRAINING_MEASURING_SCENARIO['data']['samples'][cell][elevationCell]
        except IndexError:
             pass
        
         # Object include the "data" wrapper
        return TRAINING_MEASURING_TO_RETURN

# Helpers
def init_training_scenario():
    
    if not app.config['TRAINING_ROUTES_ENABLED']:
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    training_file = os.path.join(app.config['APP_TEMP_FOLDER'], 'training.json')

    # Load training scenario file
    data = load_mapping_json_file(training_file)

    # Build training objects
    if not data:
        response_json = wrap_data({}, error="Error occurred")
        return response_json

    init_global_hash_for_training()

    # First build best hbs and evaluation results objects
    init_training_objects(data)

    # Based on the best hbs build the measuring object
    # First init measuring object 
    mockup.init_measuring(TRAINING_MEASURING_SCENARIO)
    mockup.init_measuring(TRAINING_MEASURING_TO_RETURN)

    # Modify measuring object according to current scenario
    for hbs in TRAINING_BEST_HBS["HBS"]:
        if hbs['cursorLocation']['elevation'] and hbs['cursorLocation']['horizontal']:
            elevation = hbs['cursorLocation']['elevation']
            horizontal = hbs['cursorLocation']['horizontal']
            cursor_location = getTrainingCursorLocation(horizontal, elevation)
            cell = cursor_location['cellNumber']

            if cursor_location['elevationCell'] == 'high':
                set_cell_to_true(cell,'elevationHigh')

            if cursor_location['elevationCell'] == 'middle':
                set_cell_to_true(cell, 'elevationMedium')

            if cursor_location['elevationCell'] == 'low':
                set_cell_to_true(cell, 'elevationLow')

def set_cell_to_true(cell, elevation):
    TRAINING_MEASURING_SCENARIO["data"]["samples"][cell][elevation]['scanned'] = "true"
    TRAINING_MEASURING_SCENARIO["data"]["samples"][cell][elevation]['sectorFound'] = "true"
    TRAINING_MEASURING_SCENARIO["data"]["samples"][cell][elevation]['sectorWithNetwork'] = "true"
    TRAINING_MEASURING_SCENARIO["data"]["samples"][cell][elevation]['sectorWithSpecSectorId'] = "true"
    TRAINING_MEASURING_SCENARIO["data"]["samples"][cell][elevation]['cirResourcesExist'] = "true"
    TRAINING_MEASURING_SCENARIO["data"]["samples"][cell][elevation]['beResourcesExist'] = "true"

def init_training_objects(data):

    TRAINING_BEST_HBS["HBS"] = [];

    for hbs in data["HBS"]:
        TEMP = {}
        TEMP_FINE_ALIGNMENT = {}
        for key in hbs:
            # Evaluation results
            if key == 'DownLink' or key == 'UpLink':
                TRAINING_EVALUATION_RESULTS[key] = hbs[key]
            # Fine Alignment
            if key == 'FineBestRss' or key == 'FineElevation' or key =='FineHorizontal':
                TEMP_FINE_ALIGNMENT[key] = hbs[key]
            else:
                TEMP[key] = hbs[key]

        # Calculate cursor location
        cursor_location = getTrainingCursorLocation(TEMP['cursorLocation']['horizontal'], TEMP['cursorLocation']['elevation'])
        TEMP['cursorLocation'] = cursor_location
        TRAINING_BEST_HBS["HBS"].append(TEMP)
        TRAINING_FINE_ALIGNMENT.append(TEMP_FINE_ALIGNMENT)

    if 'HSU' in data:
        TRAINING_INITIAL_DATA['azimutBeamwidth'] = data['HSU']['azimutBeamwidth']
        TRAINING_INITIAL_DATA['elevationBeamwidth'] = data['HSU']['elevationBeamwidth']
        TRAINING_INITIAL_DATA['hsuId'] = data['HSU']['hsuId']
        TRAINING_INITIAL_DATA['hsuLinkState'] = data['HSU']['hsuLinkState']
        TRAINING_INITIAL_DATA['hsuServiceType'] = data['HSU']['hsuServiceType']
        TRAINING_INITIAL_DATA['numOfElevationZones'] = data['HSU']['numOfElevationZones']
        TRAINING_INITIAL_DATA['radiusInstallConfirmationRequired'] = data['HSU']['radiusInstallConfirmationRequired']


def switch_to_mode(mode):

    config_file = os.path.join(app.config['ROOT_DIR'], 'config.py')
    f = open(config_file,'r')
    filedata = f.read()
    f.close()

    if mode == TRAINING_MODE:
        newdata = filedata.replace("app.config.from_object(ProductionConfig)","app.config.from_object(TrainingConfig)")

    if mode == PRODUCTION_MODE:
        newdata = filedata.replace("app.config.from_object(TrainingConfig)","app.config.from_object(ProductionConfig)")

    f = open(config_file,'w')
    f.write(newdata)
    f.close()

def init_global_hash_for_training():

    if not TRAINING_GLOBAL_HASH['horizontalStartAngle']:
        TRAINING_GLOBAL_HASH['horizontalStartAngle'] = -175

    if not TRAINING_GLOBAL_HASH['horizontalEndAngle']:
        TRAINING_GLOBAL_HASH['horizontalEndAngle'] = 185

    if not TRAINING_GLOBAL_HASH['horizontalScanStep']:
        TRAINING_GLOBAL_HASH['horizontalScanStep'] = 10

    if not TRAINING_GLOBAL_HASH['tableCellCount']:
        TRAINING_GLOBAL_HASH['tableCellCount'] = 36
    
    if not EVALUATION_RESULTS_STACK:
        EVALUATION_RESULTS_STACK.append(1)
        EVALUATION_RESULTS_STACK.append(2)
        EVALUATION_RESULTS_STACK.append(3)
        EVALUATION_RESULTS_STACK.append(4)
        EVALUATION_RESULTS_STACK.append(5)
        EVALUATION_RESULTS_STACK.append(6)
        EVALUATION_RESULTS_STACK.append(7)
        EVALUATION_RESULTS_STACK.append(8)
        EVALUATION_RESULTS_STACK.append(9)

def calculateTrainingCursorLocation():
    attributes_list = []
    cursorLocation = None

    try:
        attributes_list = [attributeshelper.alignment_horizontal_angle,
                           attributeshelper.alignment_elevation_angle]
                   
        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)

        if not bool(ubus_attributes_dict):
            print("Error: Unable to get alignmentHorizontalAngle and alignmentElevationAngle")
            return None

        currentHorizontalAngle = ubus_attributes_dict[attributeshelper.alignment_horizontal_angle['name']]
        currentElevationAngle  = ubus_attributes_dict[attributeshelper.alignment_elevation_angle['name']]

        cursorLocation = getTrainingCursorLocation(currentHorizontalAngle, currentElevationAngle)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        return None

    return cursorLocation

def getTrainingCursorLocation(currentHorizontalAngle, currentElevationAngle):

    horizontalCellNumber = 0
    verticalCellName = 'middle'

    for horizontalCellCount in range(0, TRAINING_GLOBAL_HASH['tableCellCount']):
        if (TRAINING_GLOBAL_HASH['horizontalStartAngle'] + TRAINING_GLOBAL_HASH['horizontalScanStep'] * horizontalCellCount) >= int(currentHorizontalAngle):
            horizontalCellNumber = horizontalCellCount
            break

    if int(currentElevationAngle) > (TRAINING_GLOBAL_HASH['elevationBeamwidth'] / 2):
        verticalCellName = 'high'

    if int(currentElevationAngle) < -(TRAINING_GLOBAL_HASH['elevationBeamwidth'] / 2):
        verticalCellName = 'low'

    _cursorLocation = {'cellNumber': int(horizontalCellNumber),
                      'elevationCell': verticalCellName,
                      'elevation': int(currentElevationAngle),
                      'horizontal': int(currentHorizontalAngle)}

    return _cursorLocation

init_training_scenario()
