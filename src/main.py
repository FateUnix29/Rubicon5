#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                                    Rubicon 5                                                                    ##
##                                              The latest step in your favorite lunatic Discord bot.                                              ##
##                                                                                                                                                 ##
##                                   Started by Kalinite, with contributions and forks from the lovely community.                                  ##
##                                                      https://github.com/FateUnix29/Rubicon5                                                     ##
##                                                                                                                                                 ##
#####################################################################################################################################################

### Hard-coded Python Modules ###

import os, sys
from pathlib import Path

### Internal Source Files ###

sys.path.append(str(Path(__file__).parent.parent))
from resources.deps.dephandler import *
from resources.deps.dependencydefs import *

### Hard Dependencies ###

with hard_dependency("Rubicon", hard_dependencies): import discord

### Soft Dependencies ###

with soft_dependency("Rubicon", soft_dependencies): import groq
with soft_dependency("Rubicon", soft_dependencies): import ollama
with soft_dependency("Rubicon", soft_dependencies): import logging