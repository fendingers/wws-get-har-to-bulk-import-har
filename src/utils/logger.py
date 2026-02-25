"""
Centralized logger setup.
"""

import logging
import logging.config

def get_logger(name):
    logging.config.fileConfig("config/logging.conf")
    return logging.getLogger(name)
