"""
*******************************************************************************
 File: src/utils/logger.py
 Purpose: Set logging defaults for consistent logging across the application.
 Source: "config/logging" contains the logging defaults
 Author: fendingers (ITS) | Contact: fendingers@ecc.edu | 716-851-1828
 Version: 1.0 | Date: 2026-02-25
*******************************************************************************
    Date           Change Description
    MM-DD-YYYY     Provide a meaningful description of what you changed and why
*******************************************************************************
    02/25/2026      Initial Version. ECC - fendingers
    02/26/2026      Reformat 80 col. ECC - fendingers
*******************************************************************************
 get_logger(): Creates a new logger with the input name. 
 _configure_logging(): Ensures that logging is not initialized more than once.
 _fallback_basic_config(): Sets the lets the fallback logging format.
*******************************************************************************
"""

import logging
import logging.config
import src.utils.path_utils as path_mod
from threading import Lock


# Boolean stores whether logger config is already loaded, and lock is 
# a centralized instance.
_LOGGING_CONFIGURED = False
_LOCK = Lock()



def _fallback_basic_config() -> None:
    """Provide a sane default if logging.conf is unavailable."""
    
    # Set the default config
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )


def _configure_logging():
    """
    Configure logging exactly once.
    - Uses path_mod.ConfNames.LOGGING_CONF
    - Falls back to basicConfig if missing/invalid
    - Captures Python warnings
    """
    
    # TODO: Open logger in another window
    # TODO: Have Logger handle ALL unhandled exceptions
    
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return
        
    # Everything beyond this point is locked to one thread
    with _LOCK:
        # Re-checking that _LOGGING_CONFIGURED wasn't set during the lock
        # acquisition
        if _LOGGING_CONFIGURED:
            return
        
        try:
            # get_dir_path must be in a try/except block
            config_path = path_mod.get_dir_path(
                path_mod.DirNames.CONFIG_DIR
            )
            
            # Set logging fileConfig to config_path
            logging.config.fileConfig(
                str(config_path), 
                disable_existing_loggers=False
            )
            
        except FileNotFoundError:
            _fallback_basic_config()
            
            # Warn about file not found
            logging.getLogger(__name__).warning(
                "WARN: Logging config not found at " +
                path_mod.DirNames.CONFIG_DIR +
                "; using basicConfig()"
            )
            
        except Exception as e:
            _fallback_basic_config()
            
            # Notify of other exceptions
            logging.getLogger(__name__).exception(
                "ERROR: Failed to configure logging from " +
                path_mod.DirNames.CONFIG_DIR +
                "; using basicConfig(). Error: " +
                str(e)
            )
                
        # Route warnings through logging
        logging.captureWarnings(True)
        
        _LOGGING_CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with the given name. 
    Logging is configured only once.
    """
    _configure_logging()
    return logging.getLogger(name)
