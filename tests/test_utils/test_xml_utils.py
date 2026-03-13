"""
*******************************************************************************
 File: tests/test_utils/test_xml_utils.py
 Purpose: Contain test functions for xml_utils.py
 Source: N/A - Values are coded in this file.
 Author: fendingers (ITS) | Contact: fendingers@ecc.edu | 716-851-1828
 Version: 1.0 | Date: 2026-03-03
*******************************************************************************
    Date           Change Description
    MM-DD-YYYY     Provide a meaningful description of what you changed and why
*******************************************************************************
    03/03/2026      Initial Version. ECC - fendingers
*******************************************************************************
 test_get_settings(): Calls project_root() and logs output.
*******************************************************************************
"""


import utils.path_utils as path_mod
import utils.xml_utils as xml_mod
import utils.logger as logger_mod


def test_get_settings():
    """
    Calls get_settings() and logs file contents.
    """
    
    try:
        logger_mod.get_logger().info(
            "Found XML settings.yaml file containing: " +
            xml_mod.get_settings()
        )
    
    except:
        logger_mod.get_logger().exception(
            "ERROR: Could not find settings.yaml file at: " +
            str(path_mod.get_file_path(
                path_mod.ConfNames.SETTINGS,
                path_mod.DirNames.CONFIG_DIR
            ))
        )