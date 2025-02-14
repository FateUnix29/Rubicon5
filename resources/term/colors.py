#####################################################################################################################################################
##                                                                                                                                                 ##
##                                                         Rubicon 5 Source File: colors.py                                                        ##
##                                     Definitions for terminal colors. Also overrides a builtin to clear them.                                    ##
##                                                                                                                                                 ##
#####################################################################################################################################################

### Hard-coded Python Modules ###

from builtins import print as _print
import os

from resources.hooks.hooklib import modular_fn

if os.name == 'nt': os.system('color') # On NT systems, 'color' properly initializes the terminal coloring system. Specifically, this command resets the colors when ran this way.

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                    Classes                                                                    ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

class FM: # Good ol' legacy FM class from old Rubicon versions...

    # Note: This class has been slightly jumbled and obfuscated to make its physical size in lines smaller. Without this weird compacting, it is VERY long.

    reset = '\x1b[0m\x1b[49m'
    red, blue, green, yellow, purple, cyan, white, black, \
    light_blue, light_green, light_red, light_purple, light_white, light_black, \
    light_cyan, light_yellow, bold, underline, italic, reverse, strikethrough, \
    remove_color, remove_bold, remove_underline, remove_italic, remove_reverse, \
    remove_strikethrough, bg_red, bg_green, bg_blue, bg_yellow, bg_black, \
    bg_white, bg_light_red, bg_light_green, bg_light_blue, bg_light_yellow, \
    bg_light_black, bg_light_white, bg_purple, bg_light_purple, bg_cyan, bg_light_cyan = (
        '\x1b[31m', '\x1b[34m', '\x1b[32m', '\x1b[33m', '\x1b[35m', '\x1b[36m', '\x1b[37m', '\x1b[30m', '\x1b[94m', '\x1b[92m', '\x1b[91m', '\x1b[95m', '\x1b[97m',
        '\x1b[90m', '\x1b[96m', '\x1b[93m', '\x1b[1m', '\x1b[4m', '\x1b[3m', '\x1b[7m', '\x1b[9m', '\x1b[39m', '\x1b[22m', '\x1b[24m', '\x1b[23m', '\x1b[27m', '\x1b[29m',
        '\x1b[41m', '\x1b[42m', '\x1b[44m', '\x1b[43m', '\x1b[40m', '\x1b[47m', '\x1b[101m', '\x1b[102m', '\x1b[104m', '\x1b[103m', '\x1b[100m', '\x1b[107m', '\x1b[45m',
        '\x1b[105m', '\x1b[46m', '\x1b[106m'
    )
    info, success, error, warning, debug, test = (f'{bold}{light_blue}INFO{remove_bold} ', f'{bold}{light_green}SUCCESS{remove_bold} ', f'{bold}{light_red}ERROR{remove_bold} ',
    f'{bold}{light_yellow}WARNING{remove_bold} ', f'{bold}{light_purple}DEBUG{remove_bold} ', f'{bold}{light_cyan}TEST{remove_bold} ')

    infod1, infod2, infod3 = (f'{bold}{light_blue}INFO (L1){remove_bold} ', f'{bold}{light_blue}INFO (L2){remove_bold} ', f'{bold}{light_blue}INFO (L3){remove_bold} ')
    warningd1, warningd2, warningd3 = (f'{bold}{light_yellow}WARNING (L1){remove_bold} ', f'{bold}{light_yellow}WARNING (L2){remove_bold} ', f'{bold}{light_yellow}WARNING (L3){remove_bold} ')
    debugd1, debugd2, debugd3 = (f'{bold}{light_purple}DEBUG (L1){remove_bold} ', f'{bold}{light_purple}DEBUG (L2){remove_bold} ', f'{bold}{light_purple}DEBUG (L3){remove_bold} ')

    trying = f"{bold}{light_yellow}TRYING{remove_bold} "
    ginfo = f"{bold}{light_green}INFO{remove_bold} "
    yinfo = f"{bold}{light_yellow}INFO{remove_bold} "

    @staticmethod
    @modular_fn(current_globals=globals())
    def header_warn(header, msg):
        print(f"{FM.warning} {header}\n{msg}")



    @staticmethod
    @modular_fn(current_globals=globals())
    def header_error(header, msg):
        print(f"{FM.error} {header}\n{msg}")

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                   Functions                                                                   ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#


@modular_fn(current_globals=globals())
def print(*args, end='\n', reset_color=True, **kwargs):
    if reset_color: _print(*args, end=f"{end}{FM.reset}", **kwargs)
    else: _print(*args, end=f"{end}", **kwargs)