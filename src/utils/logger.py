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
 kill_logger(): Removes all of the handlers associated with a logger.
 _configure_logging(): Ensures that logging is not initialized more than once.
 _fallback_basic_config(): Sets the lets the fallback logging format.
 _open_tail_terminal(): Opens a new terminal window for the root loggerm and
 stores the output in a tail file.
*******************************************************************************
"""

import logging
import logging.config
import subprocess, re, sys, platform, os
import utils.path_utils as path_mod
from pathlib import Path
from threading import Lock


# Boolean stores whether logger config is already loaded, and lock is 
# a centralized instance.
_LOGGING_CONFIGURED = False
_LOCK = Lock()

# Gathers __name__ to be reused in all logging.getLogger() calls.
# Useful for setting as a default for get_logger().
root_logger_name = __name__


def _fallback_basic_config(log_path: Path) -> None:
    """Provide a sane default if logging.conf is unavailable."""
    
    # Resolve log path to get absolute reference
    log_path = log_path.resolve()
    
    # Set StreamHandler
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Set RotatingFileHandler
    r_file_handler = logging.handlers.RotatingFileHandler(
        str(log_path),
        "a",
        5000000,
        5,
        "utf-8"
    )
    
    # Set the default config
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[console_handler, r_file_handler]
    )
    
    
def _open_tail_terminal(log_path: Path) -> subprocess.Popen | None:
    """
    Open a new terminal window that tails the given log file.
    Returns the Popen object if launched, else None.
    """
    
    # Resolve log path to get absolute reference
    log_path = log_path.resolve()
    
    if not log_path.exists():
        # Create empty file so tail can start
        log_path.touch()

    system = platform.system()

    try:
        if system == "Windows":
            # Use PowerShell tail
            cmd = [
                "powershell",
                "-NoExit",
                "-Command",
                f"Get-Content -Path '{log_path}' -Wait -Tail 50"
            ]
            # CREATE_NEW_CONSOLE opens a separate console window
            return subprocess.Popen(
                cmd, 
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )

        elif system == "Darwin":  # macOS
            # Tell Terminal.app to run a tail command
            script = (
                'tell application "Terminal" to do script '
                f'"tail -f {log_path.as_posix()}"'
            )
            return subprocess.Popen(["osascript", "-e", script])

        else:  # Linux / Unix
            # Try common terminals; adjust to your environment if needed
            # gnome-terminal example:
            cmd = [
                "gnome-terminal", 
                "--", 
                "bash", 
                "-lc", 
                f"tail -f '{log_path}' ; exec bash"
            ]
            
            try:
                return subprocess.Popen(cmd)
            except FileNotFoundError:
                # Fallback to xterm if gnome-terminal not present
                return subprocess.Popen([
                    "xterm", 
                    "-hold", 
                    "-e", 
                    f"tail -f '{log_path}'"
                ])
                
    except Exception as e:
        print(f"Failed to open log tail terminal: {e}", file=sys.stderr)
        return None


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
        
    # Set root_logger for reuse
    root_logger = logging.getLogger(root_logger_name)
    
    try:
        # Retrieve Path object for log file
        # get_file_path must be in a try/except block
        log_path = path_mod.get_file_path(
            path_mod.ConfNames.LOG,
            path_mod.DirNames.LOG_DIR
        )
        
    except Exception as e:
        # Throw error if logger file is not found
        root_logger.exception(
            "WARN: Log file not found at " +
            path_mod.DirNames.LOG_DIR +
            "; \nError: " +
            str(e)
        )

        
    # Everything beyond this point is locked to one thread
    with _LOCK:
        # Re-checking that _LOGGING_CONFIGURED wasn't set during the lock
        # acquisition
        if _LOGGING_CONFIGURED:
            return
        
        try:
            # get_file_path must be in a try/except block
            config_path = path_mod.get_file_path(
                path_mod.ConfNames.LOGGING_CONF,
                path_mod.DirNames.CONFIG_DIR
            )
            
            # TODO: Figure out why this fails to locate the logging.conf file
            # Set logging fileConfig to config_path
            logging.config.fileConfig(
                repr(config_path),
                defaults={
                    "log_path": str(log_path)
                }
            )
            
            root_logger.info("Logger configured from file " + repr(config_path))
            
        except FileNotFoundError:
            _fallback_basic_config(log_path)
            
            # Warn about file not found
            root_logger.warning(
                "WARN: Logging config not found at " +
                str(config_path) +
                "; using basicConfig()"
            )
            
        except Exception as e:
            _fallback_basic_config(log_path)
            
            # Notify of other exceptions
            root_logger.exception(
                "ERROR: Failed to configure logging from " +
                str(config_path) +
                "; using basicConfig(). \nERROR: " +
                str(e)
            )
                
        # Route warnings through logging
        logging.captureWarnings(True)
        
        _open_tail_terminal(log_path)
        
        # Notify of logger configuration
        root_logger.info(
            "Logger configured. " +
            "Log Output Path: " +
            str(log_path)
        )
        
        _LOGGING_CONFIGURED = True


def get_logger(name: str = root_logger_name) -> logging.Logger:
    """
    Returns a logger with the given name. 
    Logging is configured only once.
    """
    
    _configure_logging()
    return logging.getLogger(name)
    

def kill_logger(name: str = root_logger_name) -> None:
    """
    Kills the provided logger's terminal window.
    """
    
    target_logger = get_logger(name)
    
    try:
        logging.close(name)
    except:
        target_logger.info("Killing the root logger...")
        
    for handler in target_logger.handlers:
        target_logger.removeHandler(handler)
