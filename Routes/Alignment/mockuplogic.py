import string
import random
import uuid
from mockupinitdata import *
from FlaskServer.utils import *

##############################
########### GET CALLS ########
##############################

def getEvaluationResults(req):
	return JSON_EVALUATION_RESULTS

def getAllBands(req):
	return JSON_GET_BANDS

def getalignment():
	return JSON_MEASURING

def getbestposition():
    return JSON_BEST_HBS

def getInitialValues(req):
    return JSON_INIT_DATA_HASH

def getLinkData(req):
    result = {}
    result['frequency'] = "5780"
    return wrap_data(result)


#gets the pointer location - this call happens once every 200mil (5 times a second) 
def getPointerLocation ():
	return JSON_POINTER_LOCATION
	
def getFineAligment():

	JSON_FINE_ALIGMENT["data"]["RSSDL"] = random.randint(-66,-63);
	JSON_FINE_ALIGMENT["data"]["RSSUL"] = random.randint(-66,-63);
	JSON_FINE_ALIGMENT["data"]["LinkState"] = "Not Synchronized"
	
	return JSON_FINE_ALIGMENT;

# Alignment Simulator Only
def resetTestData(req):
	
	JSON_RESET_TEST_DATA = {};
	JSON_RESET_TEST_DATA["status"] = "Finished";
	
	JSON_MEASURING = {};
	
	init_fine_alignment()
	init_pointer_location()
	init_get_bands()
	init_measuring(JSON_MEASURING)
	init_best_postition()
	init_evaluation_results()
	
	return JSON_RESET_TEST_DATA

def getGenerateId(req):
	
	payload = req.get_json()
	
	convtoidx = ( payload["cursorLocation"]["horizontal"] + 180 ) / 20
	elevation = payload["cursorLocation"]["elevation"]
	horizontal = payload["cursorLocation"]["horizontal"]
	
	if elevation < -5: # low elevation
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationLow"]["scanned"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationLow"]["sectorFound"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationLow"]["beResourcesExist"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationLow"]["cirResourcesExist"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationLow"]["sectorWithNetwork"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationLow"]["sectorWithSpecSectorId"] = "true"
	elif elevation > 5: # high elevation
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationHigh"]["scanned"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationHigh"]["sectorFound"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationHigh"]["beResourcesExist"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationHigh"]["cirResourcesExist"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationHigh"]["sectorWithNetwork"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationHigh"]["sectorWithSpecSectorId"] = "true"
	else : # normal elevation
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationMedium"]["scanned"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationMedium"]["sectorFound"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationMedium"]["beResourcesExist"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationMedium"]["cirResourcesExist"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationMedium"]["sectorWithNetwork"] = "true"
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationMedium"]["sectorWithSpecSectorId"] = "true"
	return JSON_MEASURING

################################
########### POST CALLS #########
################################

def genericPostResponse():
	response_json = wrap_data({}, "Done")
	return response_json

def postalignment(req):
	payload = req.get_json()
	convtoidx = ( payload["cursorLocation"]["horizontal"] + 180 ) / 20
	elevation = payload["cursorLocation"]["elevation"]
	horizontal = payload["cursorLocation"]["horizontal"]
	
	cellNumber = payload["cursorLocation"]["cellNumber"]
	elevationCell = payload["cursorLocation"]["elevationCell"]
	
	#this is for now until we have a final table size we can calculate
	#it has been done because the convtoidx is assesd by a 20 slices devition
	tableSize = 20
	
	print ("elevation is: " , elevation)
	print ("horizontal is: " , horizontal)
	
	JSON_MEASURING["data"]["cursorLocation"]["elevation"] = elevation # setting the elevation 
	JSON_MEASURING["data"]["cursorLocation"]["horizontal"] = horizontal # setting the horizontal
	
	JSON_MEASURING["data"]["cursorLocation"]["cellNumber"] = int (cellNumber) # setting the horizontal
	JSON_MEASURING["data"]["cursorLocation"]["elevationCell"] = str(elevationCell) # setting the horizontal
	
	if elevation < -45:
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationLow"]["scanned"] = "true"
	elif elevation > 45:
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationHigh"]["scanned"] = "true"
	else :
		JSON_MEASURING["data"]["samples"][convtoidx]["elevationMedium"]["scanned"] = "true"
	
	#this will also post the data for the pointer in the json box position array
	updateJsonPosition(elevation, horizontal, tableSize)
	
	return JSON_MEASURING

def updateJsonPosition (elevation, horizontal, tableSize):
	
	cellSize = 180 / (tableSize/2)  # will calculate every single cell size
	horizontalCellLocation = 0      # will hold the horizontal cell location
	verticalCellLocation = "normal" # will hold the horizontal cell location
	
	if horizontal > 0:
		horizontalCellLocation = (horizontal / cellSize) + 1 + (tableSize/2) #counts how many times sample size enters in the degrees given
		
	else: 
		horizontalCellLocation = ((horizontal+180) / cellSize) + 1 #checks at what slice we are at
		
	if elevation < -45:
		verticalCellLocation = "low"
	elif elevation > 45:
		verticalCellLocation = "high"
	else :
		verticalCellLocation = "normal"
	
	JSON_POINTER_LOCATION["data"]["cursorLocation"]["elevation"]     = str(elevation)                 #setting the elevation data in the pointer json
	JSON_POINTER_LOCATION["data"]["cursorLocation"]["horizontal"]    = str(horizontal)                #setting the horizontal data in the pointer json
	JSON_POINTER_LOCATION["data"]["cursorLocation"]["cellNumber"]    = str(horizontalCellLocation)
	JSON_POINTER_LOCATION["data"]["cursorLocation"]["elevationCell"] = verticalCellLocation