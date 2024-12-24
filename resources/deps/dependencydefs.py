#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                     Rubicon 5 Source File: dependencydefs.py                                                    ##
##                                                Definitions and descriptions for each dependency.                                                ##
##                                                                                                                                                 ##
#####################################################################################################################################################

hard_dependencies = {
    "discord": "Given $NAME's nature as a Discord bot, it requires the discord.py library, a Python library for interacting with the Discord API. \
As such, the program will now exit.",
    "traceback": "Traceback is a crucial library for debugging $NAME and understanding errors in full. It's so useful that this program won't run without it.",
    "jsonc": "$NAME doesn't just use plain .json files. A lot of the files are .jsonc instead. If $NAME were to parse it with the regular json library, it would crash.",
    "jurigged": "Jurigged is a hot code reloading library. It would be a soft dependency, but it is so highly recommended that the program won't continue without it."
}

soft_dependencies = {
    "groq": "This bot centers around an AI. This is one of the options for that feature. If it's missing, a lot of the point of this bot is lost. \
If you're interested in using $NAME with Groq, you can install it with 'pip install groq'.",

    "ollama": "This bot centers around an AI. This is one of the options for that feature. If it's missing, a lot of the point of this bot is lost. \
If you're interested in using $NAME with Ollama, you can install it with 'pip install ollama'.",

    "logging": "Logging is a library that allows $NAME to log messages to a file. It's highly recommended, for debuging purposes, and other general keeping-track-of-things purposes.",

    "blessed": "Blessed is a cool library that allows $NAME to do some pretty cool terminal interactions. Optional, but recommended."
}