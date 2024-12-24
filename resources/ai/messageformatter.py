#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                        Rubicon 5 Source File: messages.py                                                       ##
##                                           Does fancy formatting for the message to be sent to Rubicon                                           ##
##                                                                                                                                                 ##
#####################################################################################################################################################

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                External Modules                                                               ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

import datetime                                                           # Datetime      | Datetime is a useful date & time library.
import discord                                                            # Discord       | discord.py is a library for interacting with the Discord API.

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                   Functions                                                                   ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

def message_header(message: discord.Message, time: str) -> str:
    """Construct the header of a message. Does not actually include the message contents. Beware of the trailing space."""

    retstr = f"{message.author.display_name} ({message.author.name}, #{message.channel.name}, {message.guild.name} @ {time}): "
    return retstr, len(retstr)

def accurate_datetime() -> str:
    """Returns an accurate representation of the date and time in a mostly American format."""

    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S (%I:%M:%S %p)")