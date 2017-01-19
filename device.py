from datetime import datetime, timedelta
from FlaskServer.jsonutils import *
import FlaskServer.ubuscontroller as ubuscontroller
import FlaskServer.attributeshelper as attributeshelper
import FlaskServer.converters as converters

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Init device attributes
def init_device():
    global reboot_time
    global interface_number

    attributes_list = [attributeshelper.sys_up_time,
                       attributeshelper.interface_number]

    try:
        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(attributes_list)           

        if not ubus_attributes_dict:
            return None
        
        sys_up_time_string = ubus_attributes_dict[attributeshelper.sys_up_time[ubuscontroller.NAME_KEY]]
        interface_number_string = ubus_attributes_dict[attributeshelper.interface_number[ubuscontroller.NAME_KEY]]

        if sys_up_time_string:
            sys_up_time = float(sys_up_time_string)
            reboot_time = datetime.now() + timedelta(seconds=(-sys_up_time / 100))
        
        if interface_number_string:
            interface_number = int(interface_number_string)

        # Load mapping JSON file
        data = load_mapping_json_file(os.path.join(__location__, 'interfaces.json'))

        ## Add rows to table and update proper index
        inflate_table(data, 103)

        ubus_attributes_dict = ubuscontroller.get_attributes_ubus(flatten_json(data))           
            
        if not ubus_attributes_dict:
            return None


    except:
        raise
