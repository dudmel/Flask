import os
import logging
import logging.handlers
import datetime
from FlaskServer.utils import get_base_dir

class BaseConfig(object):
    """Default configuration options."""
    APP_NAME = 'ULC Web Server'
    SECRET_KEY = 'mh0rPo5L9o'
    JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=1800)
    TYPE = 'HSU' #'HBS'
    LOG_FILENAME = os.path.join(get_base_dir(), 'app.log')
    LOG_LEVEL = logging.WARNING
    USE_UBUS_C = True
    PRINT_RESPONSES = True
    PRINT_ALL = False
    LANGUAGE = 'EN'
    if os.name == 'nt': #Windows
        UPLOAD_FOLDER = os.path.join(get_base_dir(), 'temp')
        APP_TEMP_FOLDER = TEMP_FOLDER = os.path.join(get_base_dir(), 'temp')
    elif os.name == 'posix': # Linux ULC
        UPLOAD_FOLDER = os.path.join(get_base_dir(), '/common/swu/img')
        TEMP_FOLDER = os.path.join(get_base_dir(), '/tmp')
        APP_TEMP_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/temp'

    MAX_CONTENT_LENGTH = 40 * 1024 * 1024
    ROOT_DIR = get_base_dir()
    TESTING_ROUTES_ENABLED = False
    TRAINING_ROUTES_ENABLED = False
    PRODUCTION_ROUTES_ENABLED = False

class ProductionConfig(BaseConfig):
    """Production configuration options."""
    DEBUG = False
    PRODUCTION_ROUTES_ENABLED = True

class TestingConfig(BaseConfig):
    """Testing configuration options."""
    DEBUG = False
    TESTING_ROUTES_ENABLED = True

class TrainingConfig(BaseConfig):
    """Training configuration options."""
    DEBUG = False
    TRAINING_ROUTES_ENABLED = True

def configure_app(app):
    app.config.from_object(TrainingConfig)
    from flask_cors import CORS
    CORS(app, supports_credentials=True)
    # Configure logging
    file_handler = logging.handlers.RotatingFileHandler(app.config['LOG_FILENAME'], maxBytes=10000, backupCount=1)
    file_handler.setLevel(app.config['LOG_LEVEL'])
    f = OneLineExceptionFormatter('%(asctime)s|%(levelname)s|%(message)s|', '%m/%d/%Y %I:%M:%S %p')
    file_handler.setFormatter(f)
    app.logger.addHandler(file_handler)

class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result) # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s