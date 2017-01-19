from FlaskServer.Resources import en as resource

TRAP_SNMP_MODE = { 
    "1": resource.snmpv1, 
    "3": resource.snmpv3,
    # Convert back
    resource.snmpv1: "1", 
    resource.snmpv3: "3"
    }
HSU_LINK_STATE = { 
    "1": resource.linkOff,
    "2": resource.violated,
    "3": resource.unregistered,
    "4": resource.registered,
    "5": resource.authenticationError,
    "6": resource.swUpgradeRequired,
    "7": resource.registeredPassive
}
ANTENNA_TYPE = { 
    "-1": resource.antenna_none,
    "1": resource.antenna_single,
    "2": resource.antenna_dual,
    "3": resource.antenna_undefined,
    "4": resource.antenna_triple,
    # Convert back
    resource.antenna_none:      "-1",
    resource.antenna_single:    "1",
    resource.antenna_dual:      "2",
    resource.antenna_undefined: "3",
    resource.antenna_triple:    "4",
    }
ANTENNA_CONNECTION_TYPE = { 
    "-1": resource.antenna_con_type_none,
    "1": resource.antenna_con_type_external,
    "2": resource.antenna_con_type_integrated,
    "3": resource.antenna_con_type_embedded_external,
    "4": resource.antenna_con_type_embedded_integrated,
    "5": resource.antenna_con_type_integrated_bsa,
    # Convert back
    resource.antenna_con_type_none:                 "-1",
    resource.antenna_con_type_external:             "1",
    resource.antenna_con_type_integrated:           "2",
    resource.antenna_con_type_embedded_external:    "3",
    resource.antenna_con_type_embedded_integrated:  "4",
    resource.antenna_con_type_integrated_bsa:       "5"
    }
EVENTS_SEVERITY = { 
    "1": resource.events_info,
    "2": resource.events_normal,
    "4": resource.events_warning,
    "8": resource.events_minor,
    "16": resource.events_major,
    "32": resource.events_critical
    }
HSU_AIR_STATE = { 
    "2": resource.air_state_bit_failed,
    "3": resource.air_state_inactive,
    "4": resource.air_state_spectrum_measurment,
    "5": resource.air_state_scanning,
    "6": resource.air_state_cac,
    "7": resource.air_state_transceiving,
    "8": resource.air_state_stand_by,
    "9": resource.air_state_raw_alignment,
    "10": resource.air_state_unreachable
    }
LAN_CURRENT_STATUS = {
    "1": resource.lan_current_status_not_connected,
    "10": resource.lan_current_status_hd_10m,
    "11": resource.lan_current_status_fd_10m,
    "15": resource.lan_current_status_hd_100m,
    "16": resource.lan_current_status_fd_100m,
    "20": resource.lan_current_status_hd_1g,
    "21": resource.lan_current_status_fd_1g,
    "65535": resource.lan_current_status_unknown
    }
LAN_DESIRED_STATUS = {
    "1": resource.lan_desired_status_auto,
    "5": resource.lan_desired_status_auto_100m,
    "10": resource.lan_desired_status_hd_10m,
    "11": resource.lan_desired_status_fd_10m,
    "15": resource.lan_desired_status_hd_100m,
    "16": resource.lan_desired_status_fd_100m,
    "21": resource.lan_desired_status_fd_1g,
    "254": resource.lan_desired_status_disable_poe,
    "255": resource.lan_desired_status_disable,
    # Convert back
    resource.lan_desired_status_auto        : "1",
    resource.lan_desired_status_auto_100m   : "5",
    resource.lan_desired_status_hd_10m      : "10",
    resource.lan_desired_status_fd_10m      : "11",
    resource.lan_desired_status_hd_100m     : "15",
    resource.lan_desired_status_fd_100m     : "16",
    resource.lan_desired_status_fd_1g       : "21",
    resource.lan_desired_status_disable_poe : "254",
    resource.lan_desired_status_disable     : "255",
    }
WIFI_POWER_MODES = {
    "1": resource.wifi_undefined,
    "2": resource.wifi_auto,
    "3": resource.wifi_power_off,
    "4": resource.wifi_always_on,
    "5": resource.wifi_power_on,
    # Convert back
    resource.wifi_undefined  : "1",
    resource.wifi_auto   : "2",
    resource.wifi_power_off  : "3",
    resource.wifi_always_on  : "4",
    resource.wifi_power_on       : "5"
    }
WIFI_SECURITY_TYPE = {
    "1": resource.wifi_security_open,
    "2": resource.wifi_security_wep,
    "3": resource.wifi_security_wpa2,
    # Convert back
    resource.wifi_security_open  : "1",
    resource.wifi_security_wep   : "2",
    resource.wifi_security_wpa2  : "3",
    }
WIFI_AP_STATUS = {
    "1": resource.wifi_staus_off,
    "2": resource.wifi_staus_on,
    "3": resource.wifi_staus_connected,
    # Convert back
    resource.wifi_staus_off  : "1",
    resource.wifi_staus_on   : "2",
    resource.wifi_staus_connected  : "3",
    }
SPECTRUM_CHANNEL_SCANNED = {
    "1": resource.channel_not_scanned,
    "2": resource.channel_scanned,
    # Convert back
    resource.channel_not_scanned  : "1",
    resource.channel_scanned      : "2",
    }

SERVICE_HSU_TYPE = {
    '1': resource.hsu_type_fixed,
    '2': resource.hsu_type_stationary,
    '3': resource.hsu_type_mobile,
    '4': resource.hsu_type_transport,
    '5': resource.hsu_type_mobile_channel,
    '6': resource.hsu_type_residential,
    '7': resource.hsu_type_new_fixed,
    '8': resource.hsu_type_new_residential,
     # Convert back
     resource.hsu_type_fixed           : '1',
     resource.hsu_type_stationary      : '2',
     resource.hsu_type_mobile          : '3',
     resource.hsu_type_transport       : '4',
     resource.hsu_type_mobile_channel  : '5',
     resource.hsu_type_residential     : '6',
     resource.hsu_type_new_fixed       : '7',
     resource.hsu_type_new_residential : '8',
    }

ATPC_STATUSES = {
    '0': 'Off',
    '1': 'Max',
    '2': 'Min',
    '3': 'Dynamic',
    'Off':     '0',
    'Max':     '1',
    'Min':     '2',
    'Dynamic': '3',
}

SWU_STATUS = { 
    "1": "None",
    "2": "In Progress",
    "3": "Pending Reset",
    "4": "Error",
    # Convert back
    "None":             "1",
    "In Progress":      "2",
    "Pending Reset":    "3",
    "Error":            "4",
}

SWU_TYPE = { 
    "1": "SWU",
    "2": "RESTORE",
    # Convert back
    "SWU":           "1",
    "RESTORE":       "2",
}