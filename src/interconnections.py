#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                    Rubicon 5 Source File: interconnections.py                                                   ##
##        An extremely important file at the heart of Rubicon. It's like a bridge, a data tunnel between files. It imports the very minimum.       ##
##                                                                                                                                                 ##
#####################################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                           Hard-coded Python Modules                                                           ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

import os, sys                                                            # OS and System | System-specific parameters and functions, as well as path manipulation
from pathlib import Path                                                  # Path          | Manipulate path-like objects

from os.path import \
    dirname, join as pjoin, exists, isfile, isdir, basename, realpath     # OS and System | Path manipulation.

import time, datetime                                                     # Time          | Time functions
from src.modularity import *                                              # Modules       | The experimental RB5 modularity system, including live patching.

from copy import deepcopy                                                 # Copy          | Create a deep copy of an object

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                             Internal Source Files                                                             ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

sys.path.append(str(Path(__file__).parent.parent))

from resources.deps.dephandler import *
from resources.deps.dependencydefs import *
from resources.term.colors import *

from resources.safe.ioutils import *

from src import base

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                External Modules                                                               ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

### Hard Dependencies ###

with hard_dependency("Rubicon", hard_dependencies): import discord
with hard_dependency("Rubicon", hard_dependencies): import traceback
from discord import app_commands

### Soft Dependencies ###

logging_available = False
groq_available = False

with soft_dependency("Rubicon", soft_dependencies): import logging; logging_available = True
with soft_dependency("Rubicon", soft_dependencies): import groq; groq_available = True

# ...

#---------------------------------------------------------------------------------------------------------------------------------------------------#

### Globals (pre-init) ###

loggers = []
dirpath = dirname(realpath(__file__))
log_file_path = pjoin(dirpath, "..", "logs", f"rb-5-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log")
if not exists(dirname(log_file_path)): os.makedirs(dirname(log_file_path))

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                            Initialization: Stage 1                                                            ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

if logging_available:
    logger = logging.getLogger("rubi-5")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_file_path, "w", "utf-8")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    loggers.append(logger)

def log(level: str = "info", msg: str = "", *args, **kwargs):
    """A logging function for Rubicon 5. If logging is available, it uses the 'rubi-5' logger and logs to a file.
    If logging is not available, it does nothing.
    Also returns the given message."""

    if logging_available:
        match level:
            case "info":     logger.info(msg, *args, **kwargs)
            case "warning":  logger.warning(msg, *args, **kwargs)
            case "error":    logger.error(msg, *args, **kwargs)
            case "debug":    logger.debug(msg, *args, **kwargs)
            case "critical": logger.critical(msg, *args, **kwargs)
            case _:          logger.debug(msg, *args, **kwargs)

    return msg

def linfo(msg: str, *args, **kwargs):
    """Just calls log() with the 'info' level."""

    return log("info", msg, *args, **kwargs)

def lwarning(msg: str, *args, **kwargs):
    """Just calls log() with the 'warning' level."""

    return log("warning", msg, *args, **kwargs)

def lerror(msg: str, *args, **kwargs):
    """Just calls log() with the 'error' level."""

    return log("error", msg, *args, **kwargs)

def ldebug(msg: str, *args, **kwargs):
    """Just calls log() with the 'debug' level."""

    return log("debug", msg, *args, **kwargs)

def lcritical(msg: str, *args, **kwargs):
    """Just calls log() with the 'critical' level."""

    return log("critical", msg, *args, **kwargs)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                    Globals                                                                    ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

linfo("interconnections || Logging initialized...")

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

linfo("interconnections || Discord client initialized...")

key_info = read_jsonc_safe(pjoin(dirpath, "..", "keys.jsonc"))

if isinstance(key_info, JSONOperationFailed):
    FM.header_error("interconnections || Bad Key Information", f"The keys.jsonc file is malformed. Does it exist?\n{key_info.msg}\nPossible traceback:\n{traceback.format_exc()}")
    lcritical("interconnections || Bad Key Information" + f"\nThe keys.jsonc file is malformed. Does it exist?\n{key_info.msg}\nPossible traceback:\n{traceback.format_exc()}")
    sys.exit(1)

# Alrighty. Now, parse the key information.
if not isinstance(key_info, dict):
    FM.header_error("interconnections || Bad Key Information", f"The keys.jsonc file is malformed. Bad data type.\n{key_info}\nPossible traceback:\n{traceback.format_exc()}")
    lcritical("interconnections || Bad Key Information" + f"\nThe keys.jsonc file is malformed. Bad data type.\n{key_info}\nPossible traceback:\n{traceback.format_exc()}")
    sys.exit(1)

discord_token_unparsed = key_info.get("discord_token", None)
groq_key_unparsed = key_info.get("groq_key", None)

if discord_token_unparsed is None:
    FM.header_error("interconnections || Bad Key Information", f"The keys.jsonc file is malformed. Missing key 'discord_token'.\n{key_info}\nPossible traceback:\n{traceback.format_exc()}")
    lcritical("interconnections || Bad Key Information" + f"\nThe keys.jsonc file is malformed. Missing key 'discord_token'.\n{key_info}\nPossible traceback:\n{traceback.format_exc()}")
    sys.exit(1)

if groq_key_unparsed is None and groq_available:
    
    FM.header_warn("interconnections || Bad Key Information", f"The keys.jsonc file is malformed. Missing key 'groq_key'.\n{key_info}\nPossible traceback:\n{traceback.format_exc()}\n\n"
        + "Groq will be disabled.")
    
    lwarning("interconnections || Bad Key Information" + f"\nThe keys.jsonc file is malformed. Missing key 'groq_key'.\n{key_info}\nPossible traceback:\n{traceback.format_exc()}\n\n"
        + "Groq will be disabled.")

    groq_available = False

discord_token = os.environ.get(discord_token_unparsed)

if groq_available:
    groq_key = os.environ.get(groq_key_unparsed)
    groq_client = groq.Groq(api_key=groq_key)

else:
    print(f"{FM.warning} Groq is not available.")
    linfo("interconnections || Groq does not seem to be available!")
    groq_client = None

linfo("interconnections || Keys get!")

def get_config(path: str, update_globals: bool = False) -> dict | JSONOperationFailed:
    """Grabs the config file and returns it as a dictionary, or an error message if something goes wrong.
    Also, updates the globals of interconnections if update_globals is True."""

    val = read_jsonc_safe(path)
    
    if isinstance(val, JSONOperationFailed):
        return val

    if update_globals:
        globals().update(val)

    return val

linfo("interconnections || Grabbing config...")

conf = get_config(pjoin(dirpath, "..", "config.jsonc"), True)
ldebug(f"interconnections || Config:\n{conf}")

if not isinstance(conf, (dict, JSONOperationFailed)):
    FM.header_error("Bad Config Information", f"Config file is malformed. Bad data type.\n{conf}\nPossible traceback:\n{traceback.format_exc()}")
    lcritical("Bad Config Information" + f"\nConfig file is malformed. Bad data type.\n{conf}\nPossible traceback:\n{traceback.format_exc()}")
    sys.exit(1)

if isinstance(conf, JSONOperationFailed):
    FM.header_error("Bad Config Information", f"The config.jsonc file is malformed. Does it exist?\n{conf.msg}\nPossible traceback:\n{traceback.format_exc()}")
    lcritical("Bad Config Information" + f"\nThe config.jsonc file is malformed. Does it exist?\n{conf.msg}\nPossible traceback:\n{traceback.format_exc()}")
    sys.exit(1)

linfo("interconnections || Config grabbed successfully!")

conversation = deepcopy(base.baseconvo)
conversation[0]["content"] = conversation[0]["content"].replace(f"{{name}}", str(conf.get("bot_name", "Rubicon")))
backup_conversation = deepcopy(conversation)