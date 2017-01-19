from FlaskServer.Resources import en as resource
import random

# JSON_SECTIONS_BY_ANGLES is the angles we divide 360 by
JSON_SECTIONS_BY_ANGLES = 10;

# Global mockup data objects
JSON_MEASURING = {};
JSON_BEST_HBS = {};
JSON_POINTER_LOCATION = {};
JSON_FINE_ALIGMENT = {};
JSON_GET_BANDS = {};
JSON_EVALUATION_RESULTS = {}
JSON_INIT_DATA_HASH = {}

# JSON_POINTER_LOCATION return object for the pointer-location
def init_pointer_location():
	#defining the json for the box locations
	#the cell number is in what "slice" is the box currently pointing
	#the elevation cell is either, high, medium, or low, just to point where the box is currently pointing
	JSON_POINTER_LOCATION["data"] = {}
	JSON_POINTER_LOCATION["data"]["cursorLocation"] = {}
	JSON_POINTER_LOCATION["data"]["cursorLocation"]["elevation"] = '0'
	JSON_POINTER_LOCATION["data"]["cursorLocation"]["horizontal"] = '0'
	JSON_POINTER_LOCATION["data"]["cursorLocation"]["cellNumber"] = '0'
	JSON_POINTER_LOCATION["data"]["cursorLocation"]["elevationCell"] = "NaN"

#JSON_FINE_ALIGMENT return object for the fine-alignment
def init_fine_alignment():
	JSON_FINE_ALIGMENT["data"] = {}
	JSON_FINE_ALIGMENT["data"]["RSSDL"] = 0
	JSON_FINE_ALIGMENT["data"]["RSSUL"] = 0
	JSON_FINE_ALIGMENT["data"]["LinkState"] = 0

# JSON_GET_BANDS return object for the get-bands
def init_get_bands():
	# simulation of the json for the bands
	JSON_GET_BANDS["data"] = {}
	JSON_GET_BANDS["data"]["bandsList"] = []
	JSON_GET_BANDS["data"]["currentBandId"] = "5KJ/F58/SU/FCC/INT/BSA"
	JSON_GET_BANDS["data"]["currentCbw"] = 40

	bandIdsAndDescriptionsMockup = [
		{ "bandId": "5K/F58/SU2/50/FCC/INT/HG", "bandDescription": "5.730-5.845 GHz FCC/IC" },
		{ "bandId": "5K/F58/SU/50/IDA/INT", "bandDescription": "5.830-5.870 GHz WPC" },
		{ "bandId": "BAND5K/F51/SU/50/UNI/INT", "bandDescription": "5.150-5.335 GHz Universal" },
		{ "bandId": "BAND5K/F59/SU/50/UNI/INT", "bandDescription": "5.730-5.950 GHz Universal" },
		{ "bandId": "BAND5K/F58/CN/SU/INT", "bandDescription": "5.740-5.835 GHz MII" }]

	for x in range(0, 5):
		sample = { 
		"bandDescription": bandIdsAndDescriptionsMockup[x]["bandDescription"], 
		"bandId": bandIdsAndDescriptionsMockup[x]["bandId"], 
		"bandMaxFreq": "5845",
		"bandMinFreq": "5730",
		"bandResolution": "5",
		"channelBW5Freq":  ['5740', '5750', '5760', '5770', '5780', '5790', '5800', '5810', '5820', '5840'],
		"channelBW10Freq": ['5740', '5750', '5760', '5770', '5780', '5790', '5800', '5810', '5820', '5840'],
		"channelBW20Freq": ['5740', '5750', '5760', '5770', '5780', '5790', '5800', '5810', '5820', '5840'],
		"channelBW40Freq": ['5740', '5750', '5760', '5770', '5780', '5790', '5800', '5810', '5820', '5840'],
		"channelBW80Freq": ['5740', '5750', '5760', '5770', '5780', '5790', '5800', '5810', '5820', '5840'],
		"channelBW7Freq":  ['5740', '5750', '5760', '5770', '5780', '5790', '5800', '5810', '5820', '5840'],
		"channelBW14Freq": ['5740', '5750', '5760', '5770', '5780', '5790', '5800', '5810', '5820', '5840'],
		}
	
		JSON_GET_BANDS["data"]["bandsList"].append(sample)

# JSON_MEASURING return object for the meausuring 
def init_measuring(obj):
	
	anglesDataObject = {};
	anglesDataObject["samples"] = [];

	for x in range(0, (360 / JSON_SECTIONS_BY_ANGLES)):
		elevationLow = {
			"sectorFound": "false",
			"scanned": "false", 
			"beResourcesExist": "false",
			"cirResourcesExist": "false",
			"sectorWithNetwork": "false",
			"sectorWithSpecSectorId": "false"
			}

		elevationMedium = {
			"sectorFound": "false",
			"scanned": "false", 
			"beResourcesExist": "false",
			"cirResourcesExist": "false",
			"sectorWithNetwork": "false",
			"sectorWithSpecSectorId": "false"
			}

		elevationHigh = {
			"sectorFound": "false",
			"scanned": "false", 
			"beResourcesExist": "false",
			"cirResourcesExist": "false",
			"sectorWithNetwork": "false",
			"sectorWithSpecSectorId": "false"
			}
	
		sample = { "elevationLow": elevationLow, "elevationMedium": elevationMedium, "elevationHigh": elevationHigh }
		anglesDataObject["samples"].append(sample)

	obj["data"] = anglesDataObject

	obj["data"]["cursorLocation"] = {}
	obj["data"]["cursorLocation"]["elevation"] = '0'
	obj["data"]["cursorLocation"]["horizontal"] = '0'
	obj["data"]["cursorLocation"]["cellNumber"] = '0'
	obj["data"]["cursorLocation"]["elevationCell"] = "middle"

# JSON_BEST_HBS return object for the best-position
def init_best_postition():

	JSON_BEST_HBS["data"] = {};
	JSON_BEST_HBS["data"]["HBS"] = [];

	for x in range(0, (random.randint(1, 6))):

		channelAntennaBeamwidth  = random.randint(1, 80)
		channelSectorType  = 'Gen4'
		channelAngle  = random.randint(1, 180)
		channelElevation  = random.randint(1, 90)
		channel = random.randint(1, 16)
		cbw = random.randint(1, 130)
		bestRSS = random.randint(1, 80)
		sectorID = 'superSector'
		availableResourcesUL = int(random.randint(0, 100))
		availableResourcesDL = random.randint(0, 100)
		bestEffortEnabled = bool(random.randint(0, 1))
		latitude  = '32.32165484'
		latitude = '34.98765412'
		sectorIdMatched = bool(random.randint(0, 1))
		cellNumber = random.randint(1, 18)
		elevationCell = "low"

		HbsSample = { 
					"sectorType": channelSectorType, 
					"antennaBeamwidth": channelAntennaBeamwidth, 
					"channel": channel, 
					"channelBw": cbw, 
					"bestRSS": bestRSS, 
					"sectorID": sectorID, 
					"sectorIdMatched": bool(random.randint(0, 1)),
					"sectorDirection": 0,
					"availableResourcesUL": availableResourcesUL, 
					"availableResourcesDL": availableResourcesDL, 
					"bestEffortEnabled": bestEffortEnabled,
					"latitude": 0,
					"longitude": 0,
					"cursorLocation": {
							"cellNumber": cellNumber,
							"elevation": channelElevation,
							"elevationCell": elevationCell,
							"horizontal": channelAngle
						}
					}

		JSON_BEST_HBS["data"]["HBS"].append(HbsSample)

def init_initial_data_hash():
    JSON_INIT_DATA_HASH["data"] = {}

    JSON_INIT_DATA_HASH["data"]["hsuId"] = 7
    JSON_INIT_DATA_HASH["data"]["hsuLinkState"] = resource.unregistered
    JSON_INIT_DATA_HASH["data"]["hsuServiceType"] = resource.hsu_type_new_fixed
    JSON_INIT_DATA_HASH["data"]["azimutBeamwidth"] = 10
    JSON_INIT_DATA_HASH["data"]["elevationBeamwidth"] = 10
    JSON_INIT_DATA_HASH["data"]["numOfElevationZones"] = 3
    JSON_INIT_DATA_HASH["data"]["radiusInstallConfirmationRequired"] = 'true'

# JSON_EVALUATION_RESULTS return object for the evaluation-results
def init_evaluation_results():
	JSON_EVALUATION_RESULTS['data'] = {}
	JSON_EVALUATION_RESULTS['data']["DownLink"] = 3.5
	JSON_EVALUATION_RESULTS['data']["UpLink"] = 3.5

init_fine_alignment()
init_pointer_location()
init_get_bands()
init_measuring(JSON_MEASURING)
init_best_postition()
init_evaluation_results()
init_initial_data_hash()


