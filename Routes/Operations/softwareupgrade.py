from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge, NotFound
from flask import jsonify, send_file
from FlaskServer import app
from FlaskServer import radlogger
from FlaskServer.utils import *
from FlaskServer.Routes.Operations.infraHelpers import *
from FlaskServer.converters import *
from datetime import datetime

import FlaskServer.attributeshelper as attributeshelper
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.consts as consts
import os, time, sys
import os.path
import copy
import infraHelpers

# Timeouts
__VALIDATE_TIMEOUT_ = 180
__SWU_TIMEOUT__ = 180
__CLEAN_TIMEOUT__ = 10
__BACKUP_TIMEOUT__ = 180

def swu_validate_route(req):
    if req.method == 'GET':
        mode = None
        if 'mode' in req.args:
            mode = req.args['mode']

        return validate(mode)

def swu_upload_route(req):
    if req.method == 'POST':
        try:
            mode = None
            if 'mode' in req.args:
                mode = req.args['mode']
        
            if mode == 'swu':
                clean_command = attributeshelper.SWU_COMMAND_CLEAN_SWU
                valid_file_name = 'swu.bin'
            elif mode == 'restore':
                clean_command = attributeshelper.SWU_COMMAND_CLEAN_RESTORE
                valid_file_name = 'backup.bin'
            else:
                response_json = wrap_data({}, error="Error occurred")
                return response_json
        
            # Set clean command
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(clean_command)
            save_file_to_flash_helper()
            time.sleep(__CLEAN_TIMEOUT__)
            
            file = req.files['file']
            
            file.flush()
            os.fsync(file.fileno())
                    
            if file.filename == '':
                radlogger.log('swu_upload_route method - File name is invalid or empty', sys.exc_info())
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            if file and allowed_file(file.filename):
            
                # Change file name if needed
                file.filename = valid_file_name

                # Save file to OS
                filename = secure_filename(file.filename)
                save_file_to_flash_helper()
                
                # Wait for clean process to be finished
                time.sleep(__CLEAN_TIMEOUT__)
                
                radlogger.log('Path to store file: ' + app.config['UPLOAD_FOLDER'])

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                save_file_to_flash_helper()
            
                #Validate
                #return validate(mode)
                response = wrap_data({}, "File uploaded successfully")
                return response
        
            else:
                return return_swu_error('File type not allowed')
        
        except RequestEntityTooLarge:
            radlogger.log('swu_upload_route', sys.exc_info())
            return return_swu_error('File is too big')
        except:
            radlogger.log('swu_upload_route', sys.exc_info())
            return return_swu_error('Error occurred')

def swu_start_backup(req):
    try:

        backup_file = os.path.join(app.config['UPLOAD_FOLDER'], 'backup.bin')

        command = copy.deepcopy(attributeshelper.SWU_COMMAND_BACKUP)

        date_time = datetime.now().strftime(consts.DATE_TIME_FORMAT)
        
        command['value'] = '{0}{1},'.format(command['value'], date_time)
        
        # Set backup command
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)

        if not bool(ubus_attributes_dict):
            response_json = wrap_data({}, error="Error occurred")
            return jsonify(response_json)

        # Wait for backup process to be finished
        for x in range(0, __BACKUP_TIMEOUT__):
            
            time.sleep(1)
            
            # Get SWU status
            # During backup process status will be "In Progress"
            # When done it will return to "None"
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributeshelper.SWU_STATUS)
            swu_status = ubus_attributes_dict[attributeshelper.SWU_STATUS[ubuscontroller.NAME_KEY]]
            
            if swu_status and swu_status == SWU_STATUS['None']:
                
                if os.path.exists(backup_file):
                    return send_file(backup_file)
                else:
                    return jsonify(return_swu_error("Backup file not created"))
            
            if swu_status and swu_status == SWU_STATUS['Error']:
                return jsonify(return_swu_error())

        return jsonify(return_swu_error('Backup Failed'))

    except:
        radlogger.log('swu_start_backup', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def validate(mode):
    try:
        #data = {}
        #from_ubus = 'Type=SWU,Release=4.9.0,Description=Radwin;'
        #sd = dict(u.split("=") for u in from_ubus.strip(';').split(","))

        #data['type'] = sd['Type']
        #data['release'] = sd['Release']
        #data['description'] = sd['Description']

        #return wrap_data(data)
        #data = {"error":"err"}
        #return wrap_data(data, "no meta data exits")

        if mode == 'swu':
            command = attributeshelper.SWU_COMMAND_VALIDATE_SWU
        elif mode == 'restore':
            command = attributeshelper.SWU_COMMAND_VALIDATE_RESTORE
        else:
            response_json = wrap_data({}, error="Error occurred")
            return response_json

        # Validate
        ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)
        
        # Wait X sec
        time.sleep(__CLEAN_TIMEOUT__)

        for x in range(0, __SWU_TIMEOUT__):
            # Get status
            ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributeshelper.SWU_STATUS)

            if not bool(ubus_attributes_dict):
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            # Get Status
            swu_status = ubus_attributes_dict[attributeshelper.SWU_STATUS[ubuscontroller.NAME_KEY]]

            if not swu_status:
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            if swu_status == SWU_STATUS['None']:
                # Get Metadata
                ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributeshelper.SWU_METADATA)

                if not bool(ubus_attributes_dict):
                    response_json = wrap_data({}, error="Error occurred")
                    return response_json

                metadata = ubus_attributes_dict[attributeshelper.SWU_METADATA[ubuscontroller.NAME_KEY]]

                if metadata:
               
                    sd = dict(u.split("=") for u in metadata.strip(';').split(","))
                    data = {}
                    data['type'] = SWU_TYPE[sd['Type']]
                    data['release'] = sd['Release']
                    data['description'] = sd['Description']
                    if  mode == 'restore':
                        data['date'] = sd['Date']

                    response = wrap_data(data)
                else:
                    response = wrap_data({}, "no metadata exits")

                return response

            if swu_status and swu_status == SWU_STATUS['Error']:
                return return_swu_error()

            time.sleep(1)

        radlogger.log('validate method exit due to Timeout', None)
        return return_swu_error()

    except:
        radlogger.log('validate', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json

def swu_start_route(req):
    if req.method == 'POST':
        try:
            mode = None
            if 'mode' in req.args:
                mode = req.args['mode']
        
            if mode == 'swu':
                command = attributeshelper.SWU_COMMAND_START_UPGRADE
            elif mode == 'restore':
                command = attributeshelper.SWU_COMMAND_START_RESTORE
            else:
                response_json = wrap_data({}, error="Error occurred")
                return response_json

            # Start Process
            ubus_attributes_dict = ubuscontroller.set_attributes_ubus(command)

            # Get status for X seconds
            for x in range(0, __SWU_TIMEOUT__):
                # Get SWU status
                ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributeshelper.SWU_STATUS)
                swu_status = ubus_attributes_dict[attributeshelper.SWU_STATUS[ubuscontroller.NAME_KEY]]
            
                if swu_status and swu_status == SWU_STATUS['Pending Reset']:
                    response_json = wrap_data({}, msg="SWU completed")
                    return response_json
                if swu_status and swu_status == SWU_STATUS['Error']:
                    return return_swu_error()

                time.sleep(1)

            return return_swu_error()
        except:
            radlogger.log('swu_start_route', sys.exc_info())
            response_json = wrap_data({}, error="Error occurred")
            return response_json

def swu_check_file_existence(req):
    mode = None
    file_name = ''
    response_json = {}

    if 'mode' in req.args:
        mode = req.args['mode']
    else:
        response_json = wrap_data({}, error="No mode is passed")
        return response_json
        
    if mode == 'swu':
        file_name = 'swu.bin'
    elif mode == 'restore':
        file_name = 'backup.bin'
    else:
        response_json = wrap_data({}, error="incorrect mode was passed")
        return response_json

    response = ''
    existing_file = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    response = "true" if os.path.exists(existing_file) else "false"
    response_json = wrap_data({}, response)
    return response_json

def return_swu_error(msg=None):

    if not msg:
        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributeshelper.SWU_ERROR)
        swu_error = ubus_attributes_dict[attributeshelper.SWU_ERROR[ubuscontroller.NAME_KEY]]
    else:
        swu_error = msg
    
    if swu_error:
        response = {}
        return wrap_data({}, error=swu_error)

    return

def get_file_size(file):
    file.flush()
    return os.fstat(file.fileno()).st_size

def allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1] in ['swul']) or (filename.rsplit('.', 1)[1] in ['backupl']) 