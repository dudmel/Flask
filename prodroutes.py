"""
Routes for the flask application.
"""
from FlaskServer import app
from flask import jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from Routes.Monitor import monitor_route
from Routes.System import system_route
from Routes.Radio import radio_route
from Routes.Network import network_route
from Routes.RecentEvents import recent_events_route
from Routes.ActiveAlarms import active_alarms_route
from Routes.TrapsDestinations import trapsdestinations_route
from Routes.Debug import debug_log_route, debug_attribute_route
from Routes.Operations import *
from Routes.ChangeBand import *
from Routes.Operations.spectrum import *
from Routes.Operations.licenseactivation import *
from Routes.Operations.softwareupgrade import *
from Routes.Operations.licenseactivation import *
from Routes.Alignment.Training import training_action_invoker
from Routes.Alignment import *
from Routes.Wifi import wifi_route
import consts as consts 
########################################## Data URLS ############################################

#Monitor
@app.route(consts.MONITOR_URL, methods=['GET'])
#@jwt_required()
def monitorroute():
	return jsonify(monitor_route(request))

#System
@app.route(consts.SYSTEM_URL, methods=['GET', 'POST'])
#@jwt_required()
def systemroute():
    return jsonify(system_route(request))

#Radio
@app.route(consts.RADIO_URL, methods=['GET', 'POST'])
#@jwt_required()
def radioroute():
    return jsonify(radio_route(request))

#Network
@app.route(consts.NETWORK_URL, methods=['GET', 'POST'])
#@jwt_required()
def networkroute():
    return jsonify(network_route(request))

#Recent Events
@app.route(consts.RECENT_EVENTS_URL, methods=['GET'])
#@jwt_required()
def recenteventsroute():
    return jsonify(recent_events_route(request))

# Active Alarms
@app.route(consts.ACTIVE_ALARMS_URL, methods=['GET'])
#@jwt_required()
def activealarmstoute():
    return jsonify(active_alarms_route(request))

#Traps Destinations
@app.route(consts.TRAPS_DESTINATIONS_URL, methods=['GET', 'POST'])
#@jwt_required()
def trapsroute():
    return jsonify(trapsdestinations_route(request))

@app.route(consts.WIFI_URL, methods=['GET', 'POST'])
#@jwt_required()
def wifiroute():
    return jsonify(wifi_route(request))

########################################## Operations URLS ############################################

@app.route(consts.PING_URL, methods=['POST'])
#@jwt_required()
def pingroute():
    return jsonify(ping(request))

@app.route(consts.TRACE_URL, methods=['POST'])
#@jwt_required()
def traceroute():
    return jsonify(trace(request))

@app.route(consts.RESET_URL, methods=['POST'])
#@jwt_required()
def trace_route():
    return jsonify(odu_reset())

@app.route(consts.RESYNC_URL, methods=['POST'])
#@jwt_required()
def resync_route():
    return jsonify(resync())

@app.route(consts.DEREGISTER_URL, methods=['POST'])
#@jwt_required()
def deregisterlocalroute():
    return jsonify(deregister_local_route(request))


@app.route(consts.CHANGE_BAND_URL, methods=['GET', 'POST'])
#@jwt_required()
def dump_routing_func():
    return jsonify(changeBand(request))

@app.route(consts.SWU_UPLOAD_URL, methods=['POST'])
#@jwt_required()
def swuuploadroute():
    return jsonify(swu_upload_route(request))

@app.route(consts.SWU_VALIDATE_URL, methods=['GET'])
#@jwt_required()
def swuvalidateroute():
    return jsonify(swu_validate_route(request))

@app.route(consts.SWU_START_URL, methods=['POST'])
#@jwt_required()
def swustartroute():
    return jsonify(swu_start_route(request))

@app.route(consts.SWU_BACKUP_URL, methods=['GET'])
#@jwt_required()
def swubackuproute():
    return swu_start_backup(request)

@app.route(consts.SWU_FILE_EXISTENCE_URL, methods=['GET'])
#@jwt_required()
def swuFileExistenceRoute():
    return jsonify(swu_check_file_existence(request))

@app.route(consts.SPEED_TEST_URL + '/<action>', methods=['GET', 'POST'])
#@jwt_required()
def speedtestroute(action):
    return jsonify(speed_test(action, request))

@app.route(consts.SPECTRUM_RANGE_URL, methods=['GET'])
#@jwt_required()
def spectrumrangeroute():
    return jsonify(spectrum_range(request))

@app.route(consts.START_SPECTRUM_URL, methods=['POST'])
#@jwt_required()
def spectrumstartroute():
    return jsonify(start_spectrum(request))

@app.route(consts.STOP_SPECTRUM_URL, methods=['POST'])
#@jwt_required()
def spectrumstoproute():
    return jsonify(stop_spectrum(request))

@app.route(consts.SPECTRUM_TABLE_URL, methods=['GET'])
#@jwt_required()
def spectrumtableroute():
    return jsonify(spectrum_table(request))

@app.route(consts.DIAGNOSTICS_URL, methods=['GET'])
#@jwt_required()
def diagnostics():
    return get_diagnostics(request)

@app.route(consts.LICENSE_ACTIVATION_URL, methods=['GET', 'POST'])
#@jwt_required()
def activatelicenseroute():
    return jsonify(license_activation(request))

@app.route(consts.CHANGE_LINK_PASSWORD, methods=['POST'])
#@jwt_required()
def changelinkpasswordroute():
    return jsonify(change_link_password(request))

@app.route(consts.RESTORE_TO_DEFAULTS_URL, methods=['POST'])
#@jwt_required()
def restoretodefaultsroute():
    return jsonify(restore_to_defaults(request))
########################################## Debug URLS ############################################

@app.route(consts.DEBUG_LOG_URL, methods=['GET'])
def debuglogroute():
    return debug_log_route()

@app.route(consts.DEBUG_ATTRIBUTE_URL, methods=['GET', 'POST'])
def debugattributeurl():
    return jsonify(debug_attribute_route(request))

########################################## Alignment URLS ############################################

@app.route(consts.ALIGNMNET_MEASURING_URL, methods=['GET'])
def alignmentRoute():
	return jsonify(alignmentTable(request))

@app.route(consts.ALIGNMNET_BEST_POSITION_URL, methods=['GET'])
def bestPositionRoute():
	return jsonify(getBestPosition(request))
	
@app.route(consts.ALIGNMNET_POINTER_LOCATION_URL, methods=['GET'])
def pointerLocationRoute():
	return jsonify(pointerLocation(request))

@app.route(consts.ALIGNMNET_ACTION_URL + '/<action>', methods=['POST'])
def actionRoutActRoute(action):
	return jsonify(alignmentActionInvoker(action, request))

# /api/v1/alignment/evaluation/<action>
@app.route(consts.ALIGNMNET_LINK_EVAL_URL + '/<action>', methods=['POST'])
def getEvaluationResultsRoute(action):
	return jsonify(evaluationActionInvoker(action, request))

@app.route(consts.ALIGNMNET_GET_ALL_BANDS_URL, methods=['GET'])
def getAllBandsRoute():
	return jsonify(alignmentGetAllBands(request))

@app.route(consts.ALIGNMNET_SET_BANDS_URL, methods=['POST'])
def setbandsroute():
	return jsonify(alignmentSetBand(request))

@app.route(consts.ALIGNMNET_FINE_ALIGNMNET_URL, methods=['GET'])
def fineAligmentRoute():
	return jsonify(getFineAligmentResults(request))

@app.route(consts.ALIGNMNET_EVAL_RESULTS_URL, methods=['GET'])
def evaluationResults():
    return jsonify(getAlignmentEvalResults(request))

@app.route(consts.ALIGNMNET_INIT_VALUES, methods=['GET'])
def initValuesRoute():
    return jsonify(getInitialValues(request))

@app.route(consts.ALIGNMNET_LINK_DATA, methods=['GET'])
def linkDataRoute():
    return jsonify(getLinkData(request))

##################################### Training URLS ######################################

@app.route(consts.TRAINING_URL + '/<action>', methods=['POST'])
def trainingactionroute(action):
	return jsonify(training_action_invoker(request, action))
