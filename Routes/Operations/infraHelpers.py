import subprocess
from FlaskServer import radlogger
import os, sys

__CLEAN_TIMEOUT__ = 10

def save_file_to_flash_helper():
    try:
        if os.name == 'posix':
            # DEBUG Alex P
            subprocess.call("echo 1 > /proc/sys/vm/drop_caches", shell=True)
            subprocess.call("sync", shell=True)
        
        # End of DEBUG Alex P
    except:
        radlogger.log('save_file_to_flash_helper method.', sys.exc_info())
        response_json = wrap_data({}, error="Error occurred")
        return response_json
