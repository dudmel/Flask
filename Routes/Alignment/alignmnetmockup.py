from mockuplogic import *
from FlaskServer.utils import *
from FlaskServer import radlogger

############## MOCKUP DATA ##############

def alignmentMockup(req):
    if req.method == 'GET':
        return getalignment()
    if req.method == 'POST':
        return postalignment(req)

def setBandMockup (req):
    if req.method == 'POST':
        radlogger.log(req.data, None)
        return genericPostResponse()

def pointerlocationMockup(req):
    if req.method == 'GET':
        return getPointerLocation()

def fineAligmentMockup(req):
    if req.method == 'GET':
        return getFineAligment()

def bestpositionMockup(req):
    if req.method == 'GET':
        return getbestposition()

def alignmentActionInvokerMockup(action, req):
    radlogger.log(req.data, None)
    return genericPostResponse()

def deregisterMockup(req):
    return genericPostResponse()

def getAllBandsMockup(req):
    if req.method == 'GET':
        return getAllBands(req)

def startEvaluationMockup(action, req):
    if req.method == 'POST':
        radlogger.log(req.data, None)
        return genericPostResponse()

def getEvaluationResultsMockup(req):
    if req.method == 'GET':
        return getEvaluationResults(req)

# Alignment Simulator Only
def resetTestDataMockup(req):
    if req.method == 'POST':
        return resetTestData(req)

def generateIdMockup(req):
    if req.method == 'POST':
        return getGenerateId(req)

def getInitialValuesMockup(req):
    if req.method == 'GET':
        return getInitialValues(req)

def getLinkDataMockup(req):
    if req.method == 'GET':
        return  getLinkData(req)
    
