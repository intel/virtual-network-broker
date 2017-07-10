# Config file for logging 
import logging
import logging.handlers
import sys

class configlogging(object):

    def __init__(self):
        LOG_FILENAME = 'configagent.log'
        default_level = logging.INFO
        default_maxBytes = 1000000
        default_backupCount = 5
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s','%m/%d/%Y %I:%M:%S %p')
        self.LOG = logging.getLogger('SecmonEMSLogger')
        self.LOG.setLevel(default_level)                

        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                       maxBytes=default_maxBytes,
                                                       backupCount=default_backupCount,
                                                      )
        self.LOG.addHandler(handler)
        handler.setFormatter(formatter)

    def debug(self, msg):
        self.LOG.debug(msg)

    def info(self, msg):
        self.LOG.info(msg)

    def critical(self, msg):
        self.LOG.critical(msg)

    def error(self, msg):
        self.LOG.error(msg)

    def warning(self, msg):
        self.LOG.warning(msg)

logging_obj = configlogging()
