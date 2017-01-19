import cPickle as pickle
import json
import os
import random
import datetime

path = os.path.dirname(os.path.realpath(__file__))

#Will get or post mocked data in list.json files
def mockedDataRequest(req, type):
	if req.method == 'GET':
		json_file = 'list.json'
		folder = str(type)
		if 'spectrum' in str(type):
			json_file = str(type).split('spectrum-')[1] + '.json'
			folder = 'spectrum'
		with open(path + '/' + folder + '/' + json_file) as data_file:
			# first, look for cache
			try:
				data = pickle.load( open( str(type) + ".cache", "rb" ) )
			except:
				data = json.load(data_file)
		if str(type) == 'monitor':
			randomize_monitor(data)
		if str(type) == 'speedtest':
			randomize_speedtest(data)
		return data
	if req.method == 'POST':
		# store payload in cache
		# payload = req.get_json()
		#pickle.dump( payload, open( str(type) + ".cache", "wb" ) )
		#return payload
		return {}

def randomize_monitor(data):
	data['data']['hbsLan1RxMbps'] += random.randint(-5,5)
	data['data']['hbsLan1TxMbps'] += random.randint(-5,5)
	data['data']['hbsRss'] += random.randint(-5,5)
	data['data']['hbsTput'] += random.randint(-5,5)
	data['data']['hsuLan1RxFps'] += random.randint(-5,5)
	data['data']['hsuLan1RxMbps'] += random.randint(-5,5)
	data['data']['hsuLan1TxFps'] += random.randint(-5,5)
	data['data']['hsuLan1TxMbps'] += random.randint(-5,5)
	data['data']['hsuRss'] += random.randint(-5,5)
	data['data']['hsuTput'] += random.randint(-5,5)
	data['data']['upTime'] += random.randint(0,2)
	data['data']['realTimeAndDate'] = datetime.datetime.now().isoformat()

def randomize_speedtest(data):
	data['data']['ulSpeed'] += random.randint(-10,10)
	data['data']['dlSpeed'] += random.randint(-10,10)
