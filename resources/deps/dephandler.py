#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                       Rubicon 5 Source File: dephandler.py                                                      ##
##                                         A bunch of utilities to handle dependencies, both hard and soft.                                        ##
##                                                                                                                                                 ##
#####################################################################################################################################################

### Hard-coded Python Modules ###
import os, sys, importlib.util

if os.name == "nt":
    os.system("color") # Color correctly initializes the terminal coloring system on Windows.


def check_soft_dependencies(modules: list[str], name: str | None = None, descriptions: dict[str, str] | None = None) -> list[bool]:
    """A function for checking if soft dependencies are met, displaying a warning if not.
    
    Usage::
    >>> x_available, y_available, z_available = check_soft_dependencies([x, y, z], descriptions={"x": "...", "y": "...", "z": "..."})

    This function returns a list of bools, in the same order of `modules`.
    If the first module passed is 'x', then the first bool in the return list will be if 'x' is available or not.

    The 'descriptions' argument is a dictionary that maps module names to a custom message to be displayed if not installed.
    There is a placeholder variable, '$NAME', that will be replaced with the name passed to this function.
    """

    modules_available = [True for _ in modules]

    for i, module in enumerate(modules):

        if importlib.util.find_spec(module) is None:

            desc = descriptions.get(module, "While it technically isn't required, it's highly recommended to install it.").replace("$NAME", name)

            if name is None:
                name = "Rubicon"

            print(f"\033[93mWarning: {module}, a soft dependency of {name}, is not installed. {desc}\033[0m")

            # This module is not available.
            modules_available[i] = False

    return modules_available



def check_hard_dependencies(modules: list[str], name: str | None = None, descriptions: dict[str, str] | None = None) -> None:
    """A function for checking if hard dependencies are met, displaying an error if not.
    If a module is not found, this function will attempt to use sys.exit(1).
    
    Usage::
    >>> check_hard_dependencies([x, y, z], descriptions={"x": "...", "y": "...", "z": "..."})

    The 'descriptions' argument is a dictionary that maps module names to a custom message to be displayed if not installed.
    There is a placeholder variable, '$NAME', that will be replaced with the name passed to this context manager.
    """

    for module in modules:

        if importlib.util.find_spec(module) is None:

            if name is None:
                name = "Rubicon"

            desc = descriptions.get(module, "This is required for Rubicon to run, and as such, the program will now exit.").replace("$NAME", name)

            print(f"\033[91mError: {module}, a hard dependency of {name}, is not installed. {desc}\033[0m")
            sys.exit(1)