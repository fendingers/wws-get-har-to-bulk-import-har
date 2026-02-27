"""
*******************************************************************************
 File: tests/test_utils/test_path_utils.py
 Purpose: Contain test functions for path_utils.py
 Source: N/A - Values are coded in this file.
 Author: fendingers (ITS) | Contact: fendingers@ecc.edu | 716-851-1828
 Version: 1.0 | Date: 2026-02-27
*******************************************************************************
    Date           Change Description
    MM-DD-YYYY     Provide a meaningful description of what you changed and why
*******************************************************************************
    02/27/2026      Initial Version. ECC - fendingers
*******************************************************************************
 test_project_root(): Calls project_root() in 4 different ways.
 test_get_dir_path(): Calls get_dir_path() in 3 different ways.
 test_get_file_path(): Calls get_file_path() in 3 different ways.
*******************************************************************************
"""

import utils.path_utils as path_mod


def test_project_root(root_files=[
    path_mod.ConfNames.PYPROJECT, 
    path_mod.ConfNames.PYTEST
    ]):
    """
    Creates 4 variables from the function project_root() with a call using
    no file names, a call using the provided list of file names, with a call 
    using a single file name, and with a call using a non-existant file name.
    """
    
    dir_from_args = path_mod.project_root(tuple(root_files))
    dir_from_list = path_mod.project_root(tuple([
        path_mod.ConfNames.PYPROJECT,
        path_mod.ConfNames.PYTEST
    ]))
    
    dir_from_name  = path_mod.project_root(".gitignore")
    
    # TODO: Log this
    print(dir_from_args)
    print(dir_from_list)
    print(dir_from_name)
    
    try:
        dir_from_nonex = path_mod.project_root("notarealfile")
    except FileNotFoundError:
        # TODO: Log this
        print("Correctly raised error")
        
        
def test_get_dir_path():
    """
    Creates 3 variables from the function get_dir_path() with a call using
    a directory from the enum, a directory that isn't in the enum, and a
    nonexistent directory.
    """
    
    dir_from_enum = path_mod.get_dir_path(path_mod.DirNames.TEST_DATA)
    dir_not_enum = path_mod.get_dir_path(".dir_test")
    
    # TODO: Log this
    print(dir_from_enum)
    print(dir_not_enum)
    
    try:
        dir_not_exist = path_mod.get_dir_path("notarealdir")
    except FileNotFoundError:
        # TODO: Log this
        print("Correctly raised error")


def test_get_file_path():
    """
    Creates a 3 variables from the function get_file_path() with a call using
    a file name from the enum, a file name that isn't in the enum, and a
    nonexistent file name.
    """
    
    file_from_enum = path_mod.get_file_path(path_mod.ConfNames.LOGGING_CONF)
    file_not_enum = path_mod.get_file_path(".file_test")
    
    # TODO: Log this
    print(file_from_enum)
    print(file_not_enum)
    
    try:
        file_not_exist = path_mod.get_file_path("notarealfile")
    except FileNotFoundError:
        # TODO: Log this
        print("Correctly raised error")