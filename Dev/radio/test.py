import json
from pprint import pprint

with open('list.json') as data_file:    
    file = json.load(data_file)
    data = file['data']
    for e in data.items():
        print e