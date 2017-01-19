# Prefixes
_API_V1_PREFIX = '/api/v1'
_DATA_PREFIX = '/data'
_OPERATIONS_PREFIX = '/operations'
_DEBUG_PREFIX = '/debug'
_ALIGNMENT_PREFIX = '/alignment'
_TRAINING_PREFIX = '/training'

# Formats
DATE_TIME_FORMAT = "%d/%m/%Y %H:%M:%S"

# Capability Bitmask values
CAPABILITY_INDEX_AUTOREALIGNMENT = 0
CAPABILITY_INDEX_REMOTETRAPMODE = 1
CAPABILITY_INDEX_DYNAMIC_CHANNEL_BANDWIDTH = 2
CAPABILITY_INDEX_TTL = 3
CAPABILITY_INDEX_DHCPRELAY = 4

# Data routes
MONITOR_URL = _API_V1_PREFIX + _DATA_PREFIX + '/monitor'
SYSTEM_URL = _API_V1_PREFIX + _DATA_PREFIX + '/system'
RADIO_URL = _API_V1_PREFIX + _DATA_PREFIX + '/radio'
NETWORK_URL = _API_V1_PREFIX + _DATA_PREFIX + '/network'
RECENT_EVENTS_URL = _API_V1_PREFIX + _DATA_PREFIX + '/recent-events'
TRAPS_DESTINATIONS_URL = _API_V1_PREFIX + _DATA_PREFIX + '/traps-destinations'
WIFI_URL = _API_V1_PREFIX + _DATA_PREFIX + '/wifi'
ACTIVE_ALARMS_URL = _API_V1_PREFIX + _DATA_PREFIX + '/active-alarms'

# Operations routes
PING_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/ping'
TRACE_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/trace'
RESET_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/reset'
RESYNC_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/resync'
DEREGISTER_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/deregister'
RESTORE_TO_DEFAULTS_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/restore-to-defaults'
CHANGE_LINK_PASSWORD = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/change-link-password'
CHANGE_BAND_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/change-band'
SPEED_TEST_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/speed-test'
LICENSE_ACTIVATION_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/activate-license'
DIAGNOSTICS_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/diagnostics'

# Training
# Available actions:
# load-scenario
# start/stop -> switching from production to training mode and vice versa
TRAINING_URL = _API_V1_PREFIX + '/training'

# Spectrum
SPECTRUM_RANGE_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/spectrum/range'
START_SPECTRUM_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/spectrum/start'
STOP_SPECTRUM_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/spectrum/stop'
SPECTRUM_TABLE_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/spectrum/table'

# Software Upgrade
SWU_VALIDATE_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/software-upgrade/validate'
SWU_START_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/software-upgrade/start'
SWU_UPLOAD_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/software-upgrade/upload'
SWU_BACKUP_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/software-upgrade/backup'
SWU_FILE_EXISTENCE_URL = _API_V1_PREFIX + _OPERATIONS_PREFIX + '/software-upgrade/check-file-existence'



# Alignment routes
ALIGNMNET_MEASURING_URL         = '/api/v1/alignment/measuring'
ALIGNMNET_BEST_POSITION_URL     = '/api/v1/alignment/best-position'
ALIGNMNET_POINTER_LOCATION_URL  = '/api/v1/alignment/pointer-location'
ALIGNMNET_ACTION_URL            = '/api/v1/alignment/action'
ALIGNMNET_FINE_ALIGNMNET_URL    = '/api/v1/alignment/fine-alignment'
ALIGNMNET_GET_ALL_BANDS_URL     = '/api/v1/alignment/get-bands'
ALIGNMNET_SET_BANDS_URL         = '/api/v1/alignment/set-band'
ALIGNMNET_LINK_EVAL_URL         = '/api/v1/alignment/evaluation'
ALIGNMNET_EVAL_RESULTS_URL      = '/api/v1/alignment/evaluation-results'
ALIGNMNET_INIT_VALUES           = '/api/v1/alignment/init-values'
ALIGNMNET_LINK_DATA             = '/api/v1/alignment/link-data'
# Alignment Simulator Only
ALIGNMNET_RESET_TEST_DATA_URL   = '/api/v1/alignment/reset-data'
ALIGNMNET_GENERATE_ID_URL       = '/api/v1/alignment/generateId'

# Debug routes
DEBUG_LOG_URL = _API_V1_PREFIX + _DEBUG_PREFIX + '/log'
DEBUG_ATTRIBUTE_URL = _API_V1_PREFIX + _DEBUG_PREFIX + '/attribute'