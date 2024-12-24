#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                                    Rubicon 5                                                                    ##
##                                              The latest step in your favorite lunatic Discord bot.                                              ##
##                                                                                                                                                 ##
##                                   Started by Kalinite, with contributions and forks from the lovely community.                                  ##
##                                                      https://github.com/FateUnix29/Rubicon5                                                     ##
##                                                                                                                                                 ##
#####################################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                           Hard-coded Python Modules                                                           ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

import os, sys                                                            # OS and System | System-specific parameters and functions, as well as path manipulation
from pathlib import Path                                                  # Path          | Manipulate path-like objects

from os.path import \
    dirname, join as pjoin, exists, isfile, isdir, basename, realpath     # OS and System | Path manipulation.

import signal                                                             # Signals       | Handle system signals.

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                             Internal Source Files                                                             ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

sys.path.append(str(Path(__file__).parent.parent))

from resources.deps.dephandler import *                                   # Resources     | Dependency handler.
from resources.deps.dependencydefs import *                               # Resources     | Descriptions for dependencies.
from resources.term.colors import *                                       # Resources     | Terminal coloring system.

from src.interconnections import *                                        # Source Code   | Interconnections is a special file that connects all the source files,
#                                                                                         | managing to prevent a circular import.

import mods                                                               # Modules       | Unused. Just starts the modules.
from src.modularity import *                                              # Modules       | The experimental RB5 modularity system, including live patching.

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                External Modules                                                               ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

### Hard Dependencies ###

with hard_dependency("Rubicon", hard_dependencies): import discord
with hard_dependency("Rubicon", hard_dependencies): import jurigged

### Soft Dependencies ###

with soft_dependency("Rubicon", soft_dependencies): import groq # i promise i will fix this and it wont look as terrible
with soft_dependency("Rubicon", soft_dependencies): import ollama # maybe it'll still be a context manager
with soft_dependency("Rubicon", soft_dependencies): import logging # probably not
#with soft_dependency("Rubicon", soft_dependencies): import blessed
    #import a, b, c

#---------------------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                            Initialization: Stage 1                                                            ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

def jinfo(msg: str, *args, **kwargs):
    """linfo() specialized for Jurigged."""

    return linfo(f"main::jurigged || {msg}", *args, **kwargs)

jurigged.watch(logger=jinfo)

print(f"{FM.ginfo} {linfo("main || Initialized (stage-1).")}")

def interrupthandle(_, __):
    linfo("main || Interrupt signal received. Cleaning up. Goodnight.")
    cleanup()
    print(f"{FM.bold}{FM.light_cyan}Goodnight.")
    sys.exit(0)

signal.signal(signal.SIGINT, interrupthandle)

linfo("main || Initialized interrupt handler.")

ret = None

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                   Functions                                                                   ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

# ...

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                Discord: Events                                                                ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

@client.event
#@modular(globals_=globals(), no_call=False)
async def on_ready():
    print(f"{FM.ginfo} {linfo(f'main::on_ready || Logged in... {client.user}:{client.user.id}')}")
    await tree.sync(guild=discord.Object(id=1278530648725913611))
    print(f"{FM.ginfo} {linfo(f'main::on_ready || Synced commands...')}")
    # As of Rubicon 5, servers are NOT security-checked to see if Rubicon should be there.

    # FIXME: NON-MODULAR

@client.event
#@modular(globals_=globals(), no_call=False)
async def on_message(message):
    global ret

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                    Cleanup                                                                    ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

def cleanup():
    for logger in loggers:
        print(f"{FM.info} {linfo(f'main::cleanup || Closing logger \'{logger.name}\'...')}")
        logger.removeHandler(handler)
    handler.close()

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                    Running                                                                    ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":

    #try:
    linfo("main || Running...")
    client.run(discord_token)

    #except KeyboardInterrupt:
    #    interrupthandle(None, None)