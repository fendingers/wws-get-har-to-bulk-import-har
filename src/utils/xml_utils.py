"""
*******************************************************************************
 File: src/utils/xml_utils.py
 Purpose: Contains XML helper functions for reuse.
 Source: N/A - Values are coded in this file.
 Author: fendingers (ITS) | Contact: fendingers@ecc.edu | 716-851-1828
 Version: 1.0 | Date: 2026-03-03
*******************************************************************************
    Date           Change Description
    MM-DD-YYYY     Provide a meaningful description of what you changed and why
*******************************************************************************
    03/03/2026      Initial Version. ECC - fendingers
*******************************************************************************
 get_settings(): Load settings file once and cache the result.
*******************************************************************************
"""


import yaml
import utils.path_utils as path_mod
import utils.logger as logger_mod
from functools import lru_cache


@lru_cache(maxsize=1)
def get_settings() -> yaml.safe_load:
    """
    Load the XML settings file once and cache the result.
    """
    
    yaml_path = path_mod.get_file_path(
        path_mod.ConfNames.SETTINGS,
        path_mod.DirNames.CONFIG_DIR
    )
    
    root_logger = logger_mod.get_logger()
    
    # Try to open the XML settings file
    with open(str(yaml_path), "r") as yaml_file:
        # Log file successfully opened
        root_logger.info(
            "Loading XML config file " + 
            str(path_mod.ConfNames.SETTINGS)
        )
        
        return yaml.safe_load(yaml_file)
        
    # If file not opened, log error
    root_logger.exception(
        "ERROR: Could not find XML config file " + 
        str(path_mod.ConfNames.SETTINGS) + 
        "at: " +
        str(yaml_path)
    )
