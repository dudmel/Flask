"""
Routes for the flask application. DEV!! DEV!! DEV!! DEV!!
"""
from FlaskServer import app
from flask import jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from Dev import mockedDataRequest
import consts as consts
from Routes.Alignment import *
from Routes.Alignment.alignmnetmockup import *
from Routes.Operations import *
from Routes.Operations.spectrum import *
from Routes.Operations.licenseactivation import *
from Routes.Operations.softwareupgrade import *
from Routes.Debug import *

########################################## Alignment URLS ############################################

@app.route(consts.ALIGNMNET_MEASURING_URL, methods=['GET', 'POST'])
def alignmentroute():
	return jsonify(alignmentMockup(request))

# copy this two functions for every get or post
@app.route(consts.ALIGNMNET_BEST_POSITION_URL, methods=['GET', 'POST'])
def bestpositionroute():
	return jsonify(bestpositionMockup(request))
	
@app.route(consts.ALIGNMNET_POINTER_LOCATION_URL, methods=['GET', 'POST'])
def pointerlocationroute():
	return jsonify(pointerlocationMockup(request))

@app.route(consts.ALIGNMNET_FINE_ALIGNMNET_URL, methods=['GET'])
def fineAligmentRoute():
	return jsonify(fineAligmentMockup(request))

@app.route(consts.ALIGNMNET_ACTION_URL + '/<action>', methods=['POST'])
def actionRoutAct(action):
	return jsonify(alignmentActionInvokerMockup(action, request))

@app.route(consts.DEREGISTER_URL, methods=['POST'])
def deregister_local_route():
    return jsonify(deregisterMockup(request))
	
# added for simulation
@app.route(consts.ALIGNMNET_GET_ALL_BANDS_URL, methods=['GET'])
def alignmentGetAllBandsRoute():
	return jsonify(getAllBandsMockup(request))

@app.route(consts.ALIGNMNET_SET_BANDS_URL, methods=['POST'])
def alignmentSetBandRoute():
	return jsonify(setBandMockup(request))

#Alignment Simulator Only
@app.route(consts.ALIGNMNET_RESET_TEST_DATA_URL, methods=['POST'])
def resetData_route():
	return jsonify(resetTestDataMockup(request))

@app.route(consts.ALIGNMNET_GENERATE_ID_URL, methods=['POST'])
def generateIdroute():
	return jsonify(generateIdMockup(request))

@app.route(consts.ALIGNMNET_INIT_VALUES, methods=['GET'])
def initValuesRoute():
    return jsonify(getInitialValuesMockup(request))

@app.route(consts.ALIGNMNET_LINK_DATA, methods=['GET'])
def linkDataRoute():
    return jsonify(getLinkDataMockup(request))

##################################### Link Evaluation URLS ######################################

# /api/v1/alignment/evaluation/<action>
@app.route(consts.ALIGNMNET_LINK_EVAL_URL + '/<action>', methods=['POST'])
def getEvaluationResultsRoute(action):
	return jsonify(startEvaluationMockup(action, request))
	
@app.route(consts.ALIGNMNET_EVAL_RESULTS_URL, methods=['GET'])
def evaluationResults():
	return jsonify(getEvaluationResultsMockup(request))
	
########################################## Data URLS ############################################

#Monitor
@app.route(consts.MONITOR_URL, methods=['GET'])
#@jwt_required()
def monitor_route():
	return jsonify(mockedDataRequest(request, 'monitor'))

#System
@app.route(consts.SYSTEM_URL, methods=['GET', 'POST'])
#@jwt_required()
def system_route():
		return jsonify(mockedDataRequest(request, 'system'))

@app.route(consts.RADIO_URL, methods=['GET', 'POST'])
#@jwt_required()
def radio_route():
	return jsonify(mockedDataRequest(request, 'radio'))

@app.route(consts.NETWORK_URL, methods=['GET', 'POST'])
#@jwt_required()
def network_route():
	return jsonify(mockedDataRequest(request, 'network'))

@app.route(consts.RECENT_EVENTS_URL)
#@jwt_required()
def recentevents_route():
	return jsonify(mockedDataRequest(request, 'recent-events'))

@app.route(consts.ACTIVE_ALARMS_URL, methods=['GET'])
#@jwt_required()
def activealarmsroute():
	return jsonify(mockedDataRequest(request, 'active-alarms'))

#Traps Destinations
@app.route(consts.TRAPS_DESTINATIONS_URL, methods=['GET', 'POST'])
#@jwt_required()
def trapsroute():
	return jsonify(mockedDataRequest(request, 'traps-destinations'))

@app.route(consts.WIFI_URL, methods=['GET', 'POST'])
#@jwt_required()
def wifiroute():
	return jsonify(mockedDataRequest(request, 'wifi'))



########################################## Operations URLS ############################################

@app.route(consts.PING_URL, methods=['POST'])
#@jwt_required()
def ping_route():
	return jsonify(ping(request))

@app.route(consts.TRACE_URL, methods=['POST'])
#@jwt_required()
def trace_route():
	return jsonify(trace(request))

@app.route(consts.RESET_URL, methods=['POST'])
#@jwt_required()
def reset_route():
	return jsonify(odu_reset())

@app.route(consts.RESYNC_URL, methods=['POST'])
#@jwt_required()
def resync_route():
	return jsonify(resync())

@app.route(consts.CHANGE_BAND_URL, methods=['GET', 'POST'])
#@jwt_required()
def changeband_route():
	return jsonify(mockedDataRequest(request, 'change-band'))

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

@app.route(consts.SPEED_TEST_URL, methods=['GET','POST'])
#@jwt_required()
def speedtestroute():
	return jsonify(mockedDataRequest(request, 'speedtest'))

@app.route('/api/v1/operations/speed-test/stop', methods=['POST'])
#@jwt_required()
def speedtestroutestop():
	return jsonify(mockedDataRequest(request, 'speedtest'))

@app.route(consts.SPECTRUM_RANGE_URL, methods=['GET'])
#@jwt_required()
def spectrumrangeroute():
	return jsonify(mockedDataRequest(request, 'spectrum-range'))

@app.route(consts.START_SPECTRUM_URL, methods=['POST'])
#@jwt_required()
def spectrumstartroute():
	return jsonify(mockedDataRequest(request, 'spectrum-start'))

@app.route(consts.STOP_SPECTRUM_URL, methods=['POST'])
#@jwt_required()
def spectrumstoproute():
	return jsonify(mockedDataRequest(request, 'spectrum-stop'))

@app.route(consts.SPECTRUM_TABLE_URL, methods=['GET'])
#@jwt_required()
def spectrumtableroute():
	return jsonify(mockedDataRequest(request, 'spectrum-table'))

@app.route(consts.LICENSE_ACTIVATION_URL, methods=['GET', 'POST'])
#@jwt_required()
def activatelicenseroute():
	return jsonify(license_activation(request))

@app.route(consts.DIAGNOSTICS_URL, methods=['GET'])
#@jwt_required()
def diagnostics():
	return get_diagnostics(request)

@app.route(consts.CHANGE_LINK_PASSWORD, methods=['POST'])
#@jwt_required()
def changelinkpasswordroute():
    return jsonify(change_link_password(request))
########################################## Debug URLS ############################################

@app.route(consts.DEBUG_LOG_URL, methods=['GET'])
def debuglogroute():
	return debug_log_route()

@app.route(consts.DEBUG_ATTRIBUTE_URL, methods=['GET', 'POST'])
def debugattributeurl():
	return jsonify(debug_attribute_route(request))

