# ------------------------------------------------------------------------------
# Builtin Imports
# ------------------------------------------------------------------------------
import os
import json
import yaml
import logging
import logging.config
import time
import colorama

# Run colorama - adds support for ANSI colours on windows
colorama.init()

def default_config():
    return {
        'version': 1,
        'disable_existing_loggers': False,  # this fixes the problem

        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': '%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                #'formatter':'standard',
                'formatter': 'colored',
                'stream': 'ext://sys.stderr'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    }

# ------------------------------------------------------------------------------
# Update the logging module to use time.gmtime for UTC as standard
# ------------------------------------------------------------------------------
logging.Formatter.converter = time.gmtime


def setup_logging(type='yaml', filename='logging.yaml', level=logging.INFO, config=None):

    # check SN_LOGGING_FILENAME environment variable
    override_filename = os.getenv('SN_LOGGING_FILENAME', None)

    # check SN_LOGGING_LEVEL environment variable
    override_level = os.getenv('SN_LOGGING_LEVEL', None)

    # if an override_filename is set, use this as the configuration
    if override_filename:
        filename = override_filename

    # load the filename
    if os.path.exists(filename):
        with open(filename, 'rt') as f:
            if type == 'json':
                config = json.load(f)
            elif type == 'yaml':
                config = yaml.load(f.read())

    # Otherwise
    else:
        # Use the supplied config or default if none was provided
        if config is None:
            config = default_config()

    # apply the configuration
    logging.config.dictConfig(config)

    # capture a root logger instance
    root_logger = logging.getLogger('')

    # logging level lookup table
    level_lookup = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARN,
        'ERROR': logging.ERROR,
    }

    # set override level where applicable
    if override_level:
        level = level_lookup[override_level]

    # apply the appropriate level
    root_logger.setLevel(level)
