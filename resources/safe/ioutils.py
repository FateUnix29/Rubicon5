#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                        Rubicon 5 Source File: ioutils.py                                                        ##
##                                        Proper, error-handled IO functions, classes, and context managers.                                       ##
##                                                                                                                                                 ##
#####################################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                           Hard-coded Python Modules                                                           ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

import json

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                             Internal Source Files                                                             ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

from resources.deps.dephandler import *
from resources.deps.dependencydefs import *

from resources.hooks.hooklib import modular_fn

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                External Modules                                                               ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

check_hard_dependencies(["jsonc"], name="Rubicon", descriptions=hard_dependencies)

import jsonc

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                    Classes                                                                    ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

class JSONOperationFailed():
    """The given JSON operation has failed."""
    
    def __init__(self, msg: any):
        self.msg = msg

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                   Functions                                                                   ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

@modular_fn(current_globals=globals())
def read_json_safe(path):
    """Reads a JSON file safely, with exhaustive error handling.
    
    Arguments
    ---------
    
    path: str
        The path to the JSON file.
    
    Returns
    -------
    
    any | JSONOperationFailed
        The JSON file's contents, or an error message."""
    
    try:
    
        with open(path, "r") as f:
            return json.load(f)
    
    except FileNotFoundError:
        return JSONOperationFailed(f"File not found: {path}")
    
    except json.JSONDecodeError as e:
        return JSONOperationFailed(f"JSON decode error: {e}")
    
    except PermissionError:
        return JSONOperationFailed(f"Permission error: {path}")
    
    except OSError as e:
        return JSONOperationFailed(f"OS error: {type(e).__name__}: {e}")

    except Exception as e:
        return JSONOperationFailed(f"General exception: {type(e).__name__}: {e}")



@modular_fn(current_globals=globals())
def read_jsonc_safe(path):
    """Reads a JSONC file safely, with exhaustive error handling.
    
    Arguments
    ---------
    
    path: str
        The path to the JSON file.
    
    Returns
    -------
    
    any | JSONOperationFailed
        The JSON file's contents, or an error message."""
    
    try:
    
        with open(path, "r") as f:
            return jsonc.load(f)
    
    except FileNotFoundError:
        return JSONOperationFailed(f"File not found: {path}")
    
    except jsonc.JSONDecodeError as e:
        return JSONOperationFailed(f"JSON decode error: {e}")
    
    except PermissionError:
        return JSONOperationFailed(f"Permission error: {path}")
    
    except OSError as e:
        return JSONOperationFailed(f"OS error: {type(e).__name__}: {e}")

    except Exception as e:
        return JSONOperationFailed(f"General exception: {type(e).__name__}: {e}")



@modular_fn(current_globals=globals())
def write_file_safe(data: any, path: str):
    """Writes data to a file safely, with exhaustive error handling.
    
    Arguments
    ---------
    
    data: any
        The data to write to the file.
    
    path: str
        The path to the file."""
    
    try:
    
        with open(path, "w") as f:
            f.write(data)
            return "Success!"

    except PermissionError:
        return JSONOperationFailed(f"Permission error: {path}")
    
    except OSError as e:
        return JSONOperationFailed(f"OS error: {type(e).__name__}: {e}")

    except Exception as e:
        return JSONOperationFailed(f"General exception: {type(e).__name__}: {e}")