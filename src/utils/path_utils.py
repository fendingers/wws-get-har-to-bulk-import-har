"""
*******************************************************************************
 File: src/utils/path_utils.py
 Purpose: Safely resolves directory and file paths.
 Source: N/A - Values are coded in this file.
 Author: fendingers (ITS) | Contact: fendingers@ecc.edu | 716-851-1828
 Version: 1.0 | Date: 2026-02-27
*******************************************************************************
    Date           Change Description
    MM-DD-YYYY     Provide a meaningful description of what you changed and why
*******************************************************************************
    02/27/2026      Initial Version. ECC - fendingers
*******************************************************************************
 project_root(): Resolves the project root directory.
 get_dir_path(): Resolves the provided directory path against cached (enum).
 get_file_path(): Resolved the given file name in the given directory (enum).
 _search_for_dir(): Resolves the provided directory path (slow).
 _search_for_file(): Resolves the given file name (slow).
*******************************************************************************
"""

from functools import lru_cache
from pathlib import Path
from enum import StrEnum


# Enum for project directory names
class DirNames(StrEnum):
    PROJECT_ROOT  = "wws-get-har-to-bulk-import-har"
    CONFIG_DIR    = "config"
    DATA_DIR      = "data"
    INPUT_DIR     = "input"
    OUTPUT_DIR    = "output"
    TEMP_DIR      = "temp"
    SRC_DIR       = "src"
    EXCEL_DIR     = "excel"
    SPLITTING_DIR = "splitting"
    TRANSFORM_DIR = "transform"
    UTILS_DIR     = "utils"
    TEST_TESTS    = "tests"
    TEST_DATA     = "test_data"
    TEST_INPUT    = "test_input"
    TEST_OUTPUT   = "test_output"
    TEST_TEMP     = "test_temp"
    TEST_EXCEL    = "test_excel"
    TEST_SPLITTING= "test_splitting"
    TEST_TRANSFORM= "test_transform"
    TEST_UTILS    = "test_utils"
    
# Enum for configuration file names
class ConfNames(StrEnum):
    LOGGING_CONF = "logging.conf"
    SETTINGS     = "settings.yaml"
    TRANSFORM    = "transform.xslt"
    PYPROJECT    = "pyproject.toml"
    PYTEST       = "pytest.ini"


@lru_cache(maxsize=None)
def project_root(root_files = [ConfNames.PYPROJECT, ConfNames.PYTEST]) -> Path:
    """
    Resolve the project root directory.
    
    root_files argument expects a tuple or string.
    
    Takes the path the user started the program from (or to the current file),
    and recursively resolves to the parents directory until the provided 
    root_files are detected. Returns the path to the directory containing any
    of the root_files. Raises a FileNotFoundError if the project root is 
    not found.
    """
    
    # Path the user started the program from, or the path to the current file
    current_path = (lambda:
        Path.cwd() if DirNames.PROJECT_ROOT in str(Path.cwd())
        else Path(__file__)
        )()
        
    # If a string is input, converts to list
    if isinstance(root_files, str):
        root_files = [root_files]
        
    # Locks the root_files list to make it hashable
    if isinstance(root_files, list):
        root_files = tuple(root_files)
    
    # Loop through the parent directories, and if any directory contains any of the
    # provided root_files, returns the path to that directory.
    for parent in [current_path] + list(current_path.parents):
        
        for file_name in root_files:
            file_path = parent / file_name
            
            if file_path.exists():
                return parent

    raise FileNotFoundError(
        "ERROR: Project root directory not found. "
        "Please ensure that the project root directory is named "
        "'wws-get-har-to-bulk-import-har'."
    )


def _search_for_dir(name: str) -> Path:
    """
    Attempts to resolve the provided directory name.
    
    Returns the path to the first found matching directory. This will NOT count
    directory instances, or return multiple locations.
    
    This is slow, so it is reserved for use in get_dir_path, but is useful
    enough to be globally available. 
    
    If a frequently used directory (such as src) is added or renamed, it is
    recommended to update the DirNames enum to include it.
    """
    
    # Initialize dir_path since this function will not be handling exceptions
    dir_path = None
    
    for dir in project_root().iterdir():
        # TODO: Log this instead
        print("Searching dir '" + str(dir) + "...")
        
        dir_path = Path(dir / name)
               
        if dir_path != None and dir_path.exists():
            break
            
    return dir_path


def get_dir_path(name: str) -> Path:
    """
    Resolves the provided directory name.
    
    If the directory is not found, this will throw a FileNotFoundError. This
    function assumes the directory tree has not changed.
    """
    
    match name:
        case DirNames.PROJECT_ROOT:
            dir_path = project_root()
            
        case DirNames.CONFIG_DIR:
            dir_path = (
                project_root() / DirNames.CONFIG_DIR
            )
            
        case DirNames.DATA_DIR:
            dir_path = (
                project_root() / DirNames.DATA_DIR
            )
            
        case DirNames.INPUT_DIR:
            dir_path = (
                project_root() / DirNames.DATA_DIR / DirNames.INPUT_DIR
            )
            
        case DirNames.OUTPUT_DIR:
            dir_path = (
                project_root() / DirNames.DATA_DIR / DirNames.OUTPUT_DIR
            )
            
        case DirNames.TEMP_DIR:
            dir_path = (
                project_root() / DirNames.DATA_DIR / DirNames.TEMP_DIR
            )
            
        case DirNames.SRC_DIR:
            dir_path = (
                project_root() / DirNames.SRC_DIR
            )
            
        case DirNames.EXCEL_DIR:
            dir_path = (
                project_root() / DirNames.SRC_DIR / DirNames.EXCEL_DIR
            )
            
        case DirNames.SPLITTING_DIR:
            dir_path = (
                project_root() / DirNames.SRC_DIR / DirNames.SPLITTING_DIR
            )
            
        case DirNames.TRANSFORM_DIR:
            dir_path = (
                project_root() / DirNames.SRC_DIR / DirNames.TRANSFORM_DIR
            )
            
        case DirNames.UTILS_DIR:
            dir_path = (
                project_root() / DirNames.SRC_DIR / DirNames.UTILS_DIR
            )
            
        case DirNames.TEST_TESTS:
            dir_path = (
                project_root() / DirNames.TEST_TESTS
            )
            
        case DirNames.TEST_DATA:
            dir_path = (
                project_root() / DirNames.TEST_TESTS / DirNames.TEST_DATA
            )
            
        case DirNames.TEST_INPUT:
            dir_path = (
                project_root() / DirNames.TEST_TESTS / DirNames.TEST_DATA /
                    DirNames.TEST_INPUT
            )
            
        case DirNames.TEST_OUTPUT:
            dir_path = (
                project_root() / DirNames.TEST_TESTS / DirNames.TEST_DATA /
                    DirNames.TEST_OUTPUT
            )
            
        case DirNames.TEST_TEMP:
            dir_path = (
                project_root() / DirNames.TEST_TESTS / DirNames.TEST_DATA /
                    DirNames.TEST_TEMP
            )
            
        case DirNames.TEST_EXCEL:
            dir_path = (
                project_root() / DirNames.TEST_TESTS / DirNames.TEST_EXCEL
            )
            
        case DirNames.TEST_SPLITTING:
            dir_path = (
                project_root() / DirNames.TEST_TESTS / DirNames.TEST_SPLITTING
            )
            
        case DirNames.TEST_TRANSFORM:
            dir_path = (
                project_root() / DirNames.TEST_TESTS / DirNames.TEST_TRANSFORM
            )
            
        case DirNames.TEST_UTILS:
            dir_path = (
                project_root() / DirNames.TEST_TESTS / DirNames.TEST_UTILS
            )
            
        case _:
            dir_path = _search_for_dir(name)
            
    # If dir_path is not None, returns the Path
    if dir_path: 
        return dir_path
    
    raise FileNotFoundError(
        f"ERROR: Directory '" + name + "' not found."
    )
    
    
def _search_for_file(name: str) -> Path:
    """
    Attempts to resolve the provided filename in the existing directories.
    
    Returns the path to the first found matching file. This will NOT count
    files, or return multiple locations.
    
    This is slow, so it is reserved for use in get_file_path, but is useful
    enough to be globally available. 
    
    If a frequently used file (such as a universal excel template) is
    added or renamed, it is recommended to update the ConfNames enum to
    include it.
    """
    
    # Initialize file_path since this function will not be handling exceptions
    file_path = None
    
    for dir in DirNames:
        try:
            file_path = get_dir_path(dir) / name
            
        except FileNotFoundError:
            # TODO: Log this instead
            print("Searching dir '" + str(dir) + "...")
            continue
        
        finally:
            if file_path != None and file_path.exists():
                break
            
    return file_path
    
    
def get_file_path(name: str, dir: str = DirNames.SRC_DIR) -> Path:
    """
    Resolves the provided file name in the provided directory.
    
    If the file is not found, this will throw a FileNotFoundError. This
    function assumes the directory tree has not changed. Allows for searching
    of file withing project tree.
    """
    
    try:
        # Leaving this as a match for now. Could be looped for 
        # better maintenance.
        match name:
            case ConfNames.LOGGING_CONF:
                file_path = get_dir_path(dir) / ConfNames.LOGGING_CONF
                
            case ConfNames.SETTINGS:
                file_path = get_dir_path(dir) / ConfNames.SETTINGS
                
            case ConfNames.TRANSFORM:
                file_path = get_dir_path(dir) / ConfNames.TRANSFORM
                
            case ConfNames.PYPROJECT:
                file_path = get_dir_path(dir) / ConfNames.PYPROJECT
                
            case ConfNames.PYTEST:
                file_path = get_dir_path(dir) / ConfNames.PYTEST
                
            case _:
                file_path = get_dir_path(dir) / name
                
    except FileNotFoundError:
        file_path = _search_for_file(name, dir)
            
    # If file_path is not None, returns the Path
    if file_path: 
        return file_path
    
    raise FileNotFoundError(
        f"ERROR: File '" + name + "' not found in directory '" + 
        str(dir) + "'."
    )
    