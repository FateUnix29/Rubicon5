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
###                                                          Internal Source Files (pt1)                                                          ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

sys.path.append(str(Path(__file__).parent.parent))

from resources.deps.dephandler import *                                   # Resources     | Dependency handler.
from resources.deps.dependencydefs import *                               # Resources     | Descriptions for dependencies.

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                External Modules                                                               ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

### Hard Dependencies ###

with hard_dependency("Rubicon", hard_dependencies): import discord
with hard_dependency("Rubicon", hard_dependencies): import jurigged
with hard_dependency("Rubicon", hard_dependencies): import datetime as dt
from datetime import datetime

### Soft Dependencies ###

with soft_dependency("Rubicon", soft_dependencies): import groq # i promise i will fix this and it wont look as terrible
with soft_dependency("Rubicon", soft_dependencies): import ollama # maybe it'll still be a context manager
with soft_dependency("Rubicon", soft_dependencies): import logging # probably not
#with soft_dependency("Rubicon", soft_dependencies): import blessed
    #import a, b, c

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                          Internal Source Files (pt2)                                                          ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

# The dependency checking can get a little annoying, so basically every other source file is over here, no matter if it checks the dependencies or not.

from resources.term.colors import *                                       # Resources     | Terminal coloring system.

from src.interconnections import *                                        # Source Code   | Interconnections is a special file that connects all the source files,
#                                                                                         | managing to prevent a circular import.

import mods                                                               # Modules       | Unused. Just starts the modules.
from src.modularity import *                                              # Modules       | The experimental RB5 modularity system, including live patching.

from resources.ai.messages import *                                       # Resources     | AI message functions.
from resources.ai.messageformatter import *                               # Resources     | Functions for formatting the input to the AI.

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

def panic(message: str, *args, **kwargs):
    argsstr = ""
    
    if args:
        argsstr = ", ".join(str(arg) for arg in args)

    if kwargs:
        argsstr += f", {', '.join(f'{k}={v}' for k, v in kwargs.items())}"

    print(f"{FM.error} {lcritical(f'main::panic || {message}{f' ({argsstr})' if argsstr else ''}')}")
    print(f"{FM.error} {lcritical(f'main::panic || Rubicon is now shutting down immediately. This error is unrecoverable.')}")
    print(f"{FM.bold}{FM.light_cyan}{lcritical('As always, goodnight.')}")
    cleanup()
    sys.exit(1)

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                                Discord: Events                                                                ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

@client.event
#@modular(globals_=globals(), no_call=False)
async def on_ready():
    print(f"{FM.ginfo} {linfo(f'main::on_ready || Logged in as {client.user}:{client.user.id}...')}")
    
    await tree.sync(guild=discord.Object(id=1278530648725913611))
    
    print(f"{FM.ginfo} {linfo(f'main::on_ready || Synced commands...')}")
    
    # FIXME: NON-MODULAR
    # As of Rubicon 5, servers are NOT security checked to see if Rubicon should be there.

    curtime = int(datetime.now().strftime("%H"))
    strtime = ""
    
    if curtime < 12:
        strtime = "morning"
    
    elif curtime >= 14 and curtime < 20:
        strtime = "afternoon"
    
    else:
        strtime = "evening"

    embed = discord.Embed(
        title=f"Good {strtime}! {conf.get('bot_name', 'Rubicon')} is online!",
        color=discord.Color.yellow(),
        description="Rubicon has come online!"
    ).add_field(
        name="Version",
        value=conf.get("version", "Unknown"),
    ).add_field(
        name="Local Date",
        value=datetime.now().strftime("%m-%d-%Y"),
    ).add_field(
        name="Local Time",
        value=datetime.now().strftime("%H:%M:%S (%I:%M:%S %p)"),
    )

    if conf.get("boot_message", False):
        maybe_ping = conf.get("ping_on_boot", False)
        
        for guild in client.guilds:
            channel = discord.utils.get(guild.channels, name=conf.get("system_channel_name", "rubicon-system-messages"))
            role = discord.utils.get(guild.roles, name=conf.get("rubicon_boot_role", "Rubicon Boot Ping"))

            if channel:
                await channel.send(content=f"{(f'<@&{role.id}>' if role != None else 'No boot role found!') if maybe_ping else ''}", embed=embed)

restricted_phrases = ["[Inst]", "</s>", "<s>", "(/s)", "[deleted]", "[/s]", "[!/s]", r"<\s>", "<ignore>"]

@client.event
#@modular(globals_=globals(), no_call=False)
async def on_message(message):
    global ret, conversation, backup_conversation, conf

    # FIXME: DEEEEEFINITELY NOT MODULAR

    prompt_rubicon = True
    message_content = message.content

    starts_with_special_char = message_content.startswith(str(conf.get("special_character", "^")))
    if starts_with_special_char:
        message_content = message_content[1:]

    if message.author == client.user and not starts_with_special_char:
        ldebug("main::on_message || Message is from ourselves - No special character. Ignoring...")
        return

    if not message.guild:
        ldebug("main::on_message || Message is from a DM. Ignoring...")
        return
    
    if not message.channel.name in list(conf.get("general_channel_names", [])):
        if message.channel.name == conf.get("all_channel_name", "rubicon-all"):
            if not starts_with_special_char:
                prompt_rubicon = False
            
            # TODO conjoined message handling
        else:
            if f'<@{client.user.id}>' not in message_content and not conf.get("respond_by_default", False):
                prompt_rubicon = False

        assembled_header, header_len = message_header(message, accurate_datetime())
        full_message = f"{assembled_header}{message_content}"
        
        print(f"{FM.light_blue}{assembled_header}{FM.light_cyan}{message_content}")
        linfo(f"main::on_message || {full_message}")

    if prompt_rubicon:
        try:
            # FIXME: NON-MODULAR
            # Let's do this!
            conversation.append({"role": "user", "content": full_message})

            model = conf.get("model", "llama-3.3-70b-versatile")

            if not get_valid_groq_model(model, groq_client):
                print(f"{FM.warning} {lwarning("main::on_message || The provided model name, '{model}', is not a valid Groq model. Defaulting to llama-3.3-70b-versatile.")}")
                model = "llama-3.3-70b-versatile"

            temperature = conf.get("temperature", 0.25)
            top_p = conf.get("top_p", 0.75)
            top_k = conf.get("top_k", 40)
            frequency_penalty = conf.get("frequency_penalty", 0.00)
            presence_penalty = conf.get("presence_penalty", 0.00)
            maximum_tokens = conf.get("maximum_tokens", 32768)
            rand_msg_chance = conf.get("random_message_chance", 150)

            if groq_available and not model.startswith("ollama/"):
                linfo(f"main::on_message || Using Groq to generate response...")
                resp_content, resp_raw, tools_used = groq_message(groq_client, conversation, restricted_phrases,
                                                                  rand_msg_chance, None, model, temperature, top_p, top_k,
                                                                  frequency_penalty, presence_penalty, maximum_tokens)
                # Add to the conversation...
                conversation.append(resp_raw)
                print(f"{FM.light_yellow}Rubicon: {resp_content}")
                
                # Send the message...
                message.channel.send(resp_content)

            else:
                # Bye bye...
                panic("Ollama is not implemented! Todo!", model, "ollama/")
        
        except groq.GroqError:
            print(f"{FM.error} {lerror(f"main::on_message || Groq API returned a general error!\n{traceback.format_exc()}")}")
            message.channel.send("My brain is having some issues. Hold on, please.\n-# \"someone tell kal there is a problem with my ai\"")
        
        except groq.BadRequestError:
            print(f"{FM.error} {lerror(f"main::on_message || Groq API returned a bad request error!\n{traceback.format_exc()}")}")
            message.channel.send("I'm having issues talking to my brain. Hold on, please.\n-# \"someone tell kal there is a problem with my ai\"")
        
        except groq.RateLimitError:
            print(f"{FM.error} {lerror(f"main::on_message || We're being rate limited by Groq.\n{traceback.format_exc()}")}")
            message.channel.send("My brain is rate limiting me. Hold on, please.\n-# \"someone tell kal there is a problem with my ai\"\n-# oh and also can you tell me how to get the time remaining")
        
        except groq.UnprocessableEntityError:
            print(f"{FM.error} {lerror(f"main::on_message || Groq API returned an unprocessable entity error!\n{traceback.format_exc()}")}")
            message.channel.send("Bad sun; WHATEVER YOU just did, my brain fails to Process it; Hold on, please.;;\n-# \"someone tell kal there is a problem with my ai\"\n-# how in the hell did you get this error it should be impossible")

        except Exception:
            print(f"{FM.error} {lerror(f"main::on_message || Unknown error in message handling!\n{traceback.format_exc()}")}")
            message.channel.send("Unhandled exception in brain. Hold on, please.\n-# \"someone tell kal there is a problem with my ai\"")


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