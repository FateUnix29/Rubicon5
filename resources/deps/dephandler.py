#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                       Rubicon 5 Source File: dephandler.py                                                      ##
##                                         A bunch of utilities to handle dependencies, both hard and soft.                                        ##
##                                                                                                                                                 ##
#####################################################################################################################################################

### Hard-coded Python Modules ###
from contextlib import contextmanager
from typing import Generator
import os, sys

if os.name == "nt":
    os.system("color") # Color correctly initializes the terminal coloring system on Windows.

@contextmanager
def soft_dependency(name: str | None = None, descriptions: dict[str, str] | None = None) -> Generator[None, None, None]:
    """Context manager to handle soft dependencies, dependencies that are not required for the bot to run, but are greatly encouraged.
    Catches ``ImportError`` and prints a warning if it occurs.
    
    Usage::
    >>> with soft_dependency():
    >>>  import x, y, z

    The 'descriptions' argument is a dictionary that maps module names to a custom message to be displayed if not installed.
    There is a placeholder variable, '$NAME', that will be replaced with the name passed to this context manager.
    """

    if name is None:
        name = "Rubicon"

    try:
        yield
    except ImportError as e:
        module_name = str(e).split("'")[1] if "'" in str(e) else "Unknown Module"

        desc = descriptions.get(module_name, None)
        
        if desc is None:
            desc = "While it technically isn't required, it's highly recommended to install it."
        
        else:
            desc = desc.replace("$NAME", name)

        print(f"\033[93mWarning: {module_name}, a soft dependency of {name}, is not installed. {desc}\033[0m")

@contextmanager
def hard_dependency(name: str | None = None, descriptions: dict[str, str] | None = None) -> Generator[None, None, None]:
    """Context manager to handle hard dependencies, dependencies that are required for the bot to run.
    Catches ``ImportError`` and raises a ``SystemExit`` if it occurs.
    
    Usage::
    >>> with hard_dependency():
    >>>  import x, y, z

    The 'descriptions' argument is a dictionary that maps module names to a custom message to be displayed if not installed.
    There is a placeholder variable, '$NAME', that will be replaced with the name passed to this context manager.
    """

    if name is None:
        name = "Rubicon"


    try:
        yield
    except ImportError as e:
        module_name = str(e).split("'")[1] if "'" in str(e) else "Unknown Module"

        desc = descriptions.get(module_name, None)
        if desc is None:
            desc = "This is required for Rubicon to run, and as such, the program will now exit."

        else:
            desc = desc.replace("$NAME", name)

        print(f"\033[91mError: {module_name}, a hard dependency of {name}, is not installed. {desc}\033[0m")
        sys.exit(1)

