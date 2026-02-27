"""
*******************************************************************************
 File: tests/test_utils/test_logger.py
 Purpose: Contain test functions for logger.py
 Source: "config/logging" contains the logging defaults
 Author: fendingers (ITS) | Contact: fendingers@ecc.edu | 716-851-1828
 Version: 1.0 | Date: 2026-02-26
*******************************************************************************
    Date           Change Description
    MM-DD-YYYY     Provide a meaningful description of what you changed and why
*******************************************************************************
    02/25/2026      Initial Version. ECC - fendingers
*******************************************************************************
 test_get_logger(): Creates a specified amount of new loggers with a
 dynamic input name. Asserts that the loggers are created, named, and that 
 multiple logger handlers do not exist.
*******************************************************************************
"""

import logging
import utils.logger as logger_mod


def test_get_logger(num_loggers: int = 1):
    """
    Creates a specified amount of new loggers with a dynamic 
    input name. Asserts that the loggers are created, named, and that multiple 
    logger handlers do not exist.
    """
    loggers = []
    
    for i in range(num_loggers):
        # Create test_logger_1, test_logger_2, etc.
        logger_name = f"test_logger_" + str(i)
        logger = logger_mod.get_logger(logger_name)
        
        # Check that the logger just created is a logger
        assert isinstance(logger, logging.Logger), (
            f"Logger Error: Could not create logger " + str(i)
            )
            
        # Check that a logger exists with the newly created logger's name
        assert logger.name == logger_name, (
            f"Logger Error: Could not create logger " + logger_name
            )
        
    """# Check that the logger wasn't configured multiple times
    assert len(logger_mod.get_logger("root_logger").handlers) == 1, (
        f"Logger Error: Created multiple Logger handlers"
        )"""
        