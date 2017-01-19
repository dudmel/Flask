INTERFACE_NUMBER = {"object": 8960, "attr": 539, "index": 0, "name": "interfaceNumber"}
LAST_EVENTS_NUMBER = {"object": 9728, "attr": 1007, "index": 0, "name": "lastEventsNumber"}
ACTIVE_ALARMS_INDEXES = {"object": 9728, "attr": 1935, "index": 0, "name": "activeAlarmsIndexes"}
SYS_UP_TIME = {"object": 8960, "attr": 535, "index": 0, "name": "sysUpTime"}
HBS_COMPRESSED_MONITOR = { "object": 36608, "attr": 1222, "index": 0, "name": "hbsCompressedMonitor" }
SYS_DESCRIPTION = { "object": 8960, "attr": 644, "index": 0, "name": "sysDescription" }

COMBO_NUMBER_OF_SUBBANDS = {"object": 39936, "attr": 990, "index": 0, "name": "comboNumberOfSubBands"}
CURRENT_SUB_BAND_ID = {"object": 39936, "attr": 993, "index": 0, "name": "currentSubBandId"}

AUTHENTICATE_COMMAND = {"object": 8960, "attr": 1934, "index": 0, "value": "", "name": "authenticate"}
CHANGE_LINK_PASSWORD = {"object": 36608, "attr": 1850, "index": 0, "value": "", "name": "changeLinkPassword"}
RESTORE_TO_DEFAULTS  = {"object": 2560, "attr": 819, "index": 0, "value": "", "name": "restoreToDefaults"}

CAPABILITY_BITMASK = {"object": 2560, "attr": 1898, "index": 0, "value": "", "name": "capabilityBitmask"}

# IpParamsCnfg
IP_PARAMS_CONFIG = {"object": 2560, "attr": 874, "index": 0, "name": "ipParamsConfig"}

########## Alignment ###########
alignment_num_of_sectors_found     = {"object": 36864, "attr": 1920, "index": 0, "name": "alignmentNumOfSectorsFound"}
alignment_full_sectors_stats       = {"object": 36864, "attr": 1919, "index": 0, "name": "alignmentFullSectorsStats"}

alignment_scan_azimuth_params      = {"object": 36864, "attr": 1916, "index": 0, "name": "alignmentScanAzimuthParams"}
alignment_immediate_results_table  = {"object": 36864, "attr": 1917, "index": 0, "name": "alignmentImmediateResultsTable"}

alignment_commanding               = {"object": 36864, "attr": 1914, "index": 0, "name": "alignmentCommanding"}
alignment_set_ssid                 = {"object": 36608, "attr": 1253, "index": 0, "name": "alignmentSetSsid "}

evaluation_commanding              = {"object": 36608, "attr": 1373, "index": 0, "name": "evaluationCommanding"}

alignment_horizontal_angle         = {"object": 36864, "attr": 1612, "index": 0, "name": "alignmentHorizontalAngle"}
alignment_elevation_angle          = {"object": 36864, "attr": 1614, "index": 0, "name": "alignmentElevationAngle"}

alignment_link_state               = {"object": 36608, "attr": 1172, "index": 0, "name": "fineAlignmentLinkState"}
alignment_rss_local                = {"object": 36608, "attr": 1307, "index": 0, "name": "fineAlignmentRssLocal"}
alignment_cpeRemoteMonitorComp     = {"object": 36608, "attr": 1222, "index": 0, "name": "fineAlignmentCpeRemoteMonitorComp"}

alignment_evaluation_tput_local    = {"object": 41728, "attr":1208, "index": 0, "name": "evaluationTputLocal"}
alignment_curren_freq              = {"object": 36864, "attr":679, "index": 0, "name": "currentFrequency"}

alignment_channelBw                = {"object": 36864, "attr":803, "index": 0, "name": "alignmentChannelBw"}
alignment_available_channels_str   = {"object": 36864, "attr":664, "index": 0, "name": "alignmentAvailableChannelsStr"}
alignment_networkId                = {"object": 36608, "attr":1253, "index": 0, "name": "networkId"}
alignment_min_freq                 = {"object": 36864, "attr":659, "index": 0, "name": "alignmentMinFreq"}
alignment_max_freq                 = {"object": 36864, "attr":662, "index": 0, "name": "alignmentManFreq"}
alignment_resolution               = {"object": 36864, "attr":663, "index": 0, "name": "alignmentResolution"}
alignment_changeBandId             = {"object": 39936, "attr":993, "index": 0, "name": "changeBandId"}
alignment_geoLocation              = {"object": 36608, "attr":1391, "index": 0, "name": "geoLocation", "value": ''}
alignment_confirmInstallation      = {"object": 36608, "attr":1373, "index": 0, "name": "confirmInstallation"}


# Software Upgrade
__SWU_COMMAND = {"object": 49152, "attr": 1928, "index": 0, "name": "swuCommand"}
SWU_METADATA = {"object": 49152, "attr": 1927, "index": 0, "name": "swuMetadata"}
SWU_STATUS = {"object": 49152, "attr": 1925, "index": 0, "name": "swuStatus"}
SWU_ERROR = {"object": 49152, "attr": 1926, "index": 0, "name": "swuError"}

SWU_COMMAND_VALIDATE_SWU = __SWU_COMMAND.copy()
SWU_COMMAND_VALIDATE_RESTORE = __SWU_COMMAND.copy()
SWU_COMMAND_START_UPGRADE = __SWU_COMMAND.copy()
SWU_COMMAND_START_RESTORE = __SWU_COMMAND.copy()
SWU_COMMAND_CLEAN_SWU = __SWU_COMMAND.copy()
SWU_COMMAND_CLEAN_RESTORE = __SWU_COMMAND.copy()
SWU_COMMAND_BACKUP = __SWU_COMMAND.copy()

SWU_COMMAND_VALIDATE_SWU['value'] = '1,1,'
SWU_COMMAND_VALIDATE_RESTORE['value'] = '1,2,'
SWU_COMMAND_START_UPGRADE['value'] = '2,1,'
SWU_COMMAND_START_RESTORE['value'] = '2,2,0,'
SWU_COMMAND_CLEAN_SWU['value'] = '5,1,0,'
SWU_COMMAND_CLEAN_RESTORE['value'] = '5,2,0,'
SWU_COMMAND_BACKUP['value'] = '6,2,'

# Speed test
START_SPEED_TEST = {"object": 36608, "attr": 1373, "index": 0, "value": "101,3,1", "name": "startSpeedTest"}
STOP_SPEED_TEST = {"object": 36608, "attr": 1373, "index": 0, "value": "101,3,2", "name": "stopSpeedTest"}

RESYNC_COMMAND = {"object": 36608, "attr": 602, "index": 0, "value": "-1", "name": "resync"}

RESET_COMMAND = {"object": 2560, "attr": 215, "index": 0, "value": "3", "name": "reset"}
DEREGISTER_COMMAND = {"object": 36608, "attr": 1220, "index": 0, "value": "1", "name": "deregister"} 

# Spectrum
START_SPECTRUM = {"object": 36608, "attr": 1373, "index": 0, "value": "6", "name": "startSpectrum"}
STOP_SPECTRUM = {"object": 36608, "attr": 1373, "index": 0, "value": "7", "name": "stopSpectrum"}
AIR_CHIP_MIN_MAX_FREQ = {"object": 36864, "attr": 1374, "index": 0, "name": "airChipMinMaxFreq"}
AIR_MIN_FREQ = {"object": 36864, "attr": 659, "index": 0, "name": "airMinFreq"}
AIR_MAX_FREQ = {"object": 36864, "attr": 662, "index": 0, "name": "airMaxFreq"}
NUMBER_OF_SPECTRUM_CHANNELS = {"object": 36864, "attr": 1048, "index": 0, "name": "spectrumChannels"}

LICENSE_ACTIVATION = {"object": 2560, "attr": 995, "index": 0, "name": "licenseActivation"}