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

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                   Functions                                                                   ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

def message_header(display: str, user: str, channel: str, guild: str, time: str) -> str:
    """Construct the header of a message. Does not actually include the message contents. Beware of the trailing space."""

    retstr = f"{display} (@{user}, #{channel}, {guild} @ {time}): "
    return retstr, len(retstr)

def accurate_datetime() -> str:
    """Returns an accurate representation of the date and time in a mostly American format."""

    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S (%I:%M:%S %p)")