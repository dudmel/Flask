import os, sys
import copy
import json
from FlaskServer import app, radlogger

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def flatten_json(jsonobject):
    out_list = []
    def flatten(x, name=''):
        if type(x) is dict:
            for key, val in x.iteritems():
                if (isinstance(val, dict) or isinstance(val, list)) and not 'object' in val:
                    flatten(x[key]) # Go 1 level deeper
                else:
                    if isinstance(name, int):
                        val['name'] = key + '_' + str(val['index'])
                    else:
                        val['name'] = name + key
                    out_list.append(val)
        elif isinstance(x, list):
            i = 1
            for val in x:
                flatten(val, i)
                i += 1

    flatten(jsonobject)
    return out_list

def match_json(data, ubus_dict):
    try:
        _ubus_dict = ubus_dict

        def match(data, is_index=False):
            if type(data) is dict:
                for key, val in data.iteritems():
                    if (isinstance(val, dict) or isinstance(val, list)) and not 'object' in val: 
                        match(data[key]) # Go 1 level deeper
                    else:
                        if is_index:
                            idx_key = key + '_' + str(val['index'])
                            data[key] = _ubus_dict[idx_key]
                        else:
                            data[key] = _ubus_dict[key]
                            #if key in _ubus_dict:
                            #    data[key] = _ubus_dict[key]
            elif isinstance(data, list):
                for val in data:
                    match(val, True)

        match(data)
    except:
        radlogger.log('match_json method.', sys.exc_info())


def flatten_payload_to_dict(jsonobject):
    out_list = {} 
    def flatten(x, name=''):
        if type(x) is dict:
            for key, val in x.iteritems():
                if (isinstance(val, dict) or isinstance(val, list)) and not 'object' in val:
                    flatten(x[key]) # Go 1 level deeper
                else:
                    if isinstance(name, int):
                        key = key + '_' + str(name)

                    out_list[key] = val
        elif isinstance(x, list):
            i = 1
            for val in x:
                flatten(val, i)
                i += 1

    flatten(jsonobject)
    return out_list

def inflate_table(data, number, index = 1):
    for x in range(0, number):
        temp = copy.deepcopy(data[0])
        for key, val in temp.iteritems():
            val['index'] = index
        data.append(temp)
        index = index + 1
    data.remove(data[0])

def inflate_table_for_indexesList(data, indexesList):
    for x in range(0, len(indexesList)):
        temp = copy.deepcopy(data[0])
        for key, val in temp.iteritems():
            val['index'] = int(indexesList[x])
        data.append(temp)
    data.remove(data[0])

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def load_mapping_json_file(file):
    
    data = app.cache.get(file)

    if data is None:
        try:
            with open(os.path.join(__location__, file)) as data_file:
                data = byteify(json.load(data_file))
            app.cache.set(file, data)
        except (IOError):
            print("File not exists:" + file)
    
    return data
