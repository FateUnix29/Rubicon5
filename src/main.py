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
with hard_dependency("Rubicon", hard_dependencies): from datetime import datetime as dt

### Soft Dependencies ###

pytz_available = False

with soft_dependency("Rubicon", soft_dependencies): import groq # i promise i will fix this and it wont look as terrible
with soft_dependency("Rubicon", soft_dependencies): import ollama # maybe it'll still be a context manager
with soft_dependency("Rubicon", soft_dependencies): import logging # probably not
#with soft_dependency("Rubicon", soft_dependencies): import blessed
with soft_dependency("Rubicon", soft_dependencies): import pytz; pytz_available = True
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
    
    await tree.sync(guild=discord.Object(id=1301766861905592361))
    
    print(f"{FM.ginfo} {linfo(f'main::on_ready || Synced commands...')}")
    
    # FIXME: NON-MODULAR
    # As of Rubicon 5, servers are NOT security checked to see if Rubicon should be there.

    curtime = int(dt.now().strftime("%H"))
    strtime = ""
    
    if curtime < 14:
        strtime = "morning"
    
    elif curtime >= 14 and curtime < 20:
        strtime = "afternoon"
    
    else:
        strtime = "evening"

    # Quick little detour:
    await client.user.edit(username=conf.get("bot_name", "Rubicon"))

    embed = discord.Embed(
        title=f"Good {strtime}! {conf.get('bot_name', 'Rubicon')} is online!",
        color=discord.Color.yellow(),
        description="Rubicon has come online!"
    ).add_field(
        name="Version",
        value=conf.get("version", "Unknown"),
    ).add_field(
        name="Local Date",
        value=dt.now().strftime("%m-%d-%Y"),
    ).add_field(
        name="Local Time",
        value=dt.now().strftime("%H:%M:%S (%I:%M:%S %p)"),
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
    global ret, conversation, backup_conversation, conf, nicks

    # FIXME: DEEEEEFINITELY NOT MODULAR

    prompt_rubicon = True
    message_content = message.content
    isdm = False
    
    rubi_perceived_display = nicks.get(message.author.id, message.author.display_name)
    isnick = message.author.display_name != rubi_perceived_display
    
    rubi_perceived_name = rubi_perceived_display if isnick else message.author.name

    starts_with_special_char = message_content.startswith(str(conf.get("special_character", "^")))
    if starts_with_special_char:
        message_content = message_content[1:]

    if message.author == client.user and not starts_with_special_char:
        ldebug("main::on_message || Message is from ourselves - No special character. Ignoring...")
        return

    if not message.guild and message.author.id not in conf.get("who_can_dm_me", []):
        ldebug("main::on_message || Message is from a DM. Ignoring...")
        return

    elif not message.guild and message.author.id in conf.get("who_can_dm_me", []):
        # We shall allow DMs from this person.
        msgguild = "DM/Group DM [guild unknown]"
        channelname = "[channel unknown]"
        isdm = True
        pass

    elif message.guild:
        msgguild = message.guild.name
        channelname = message.channel.name
    
    if not channelname in list(conf.get("general_channel_names", [])):
        if channelname == conf.get("all_channel_name", "rubicon-all"):
            if not starts_with_special_char:
                prompt_rubicon = False
            
            # TODO conjoined message handling
        else:
            if f'<@{client.user.id}>' not in message_content and not isdm:
                prompt_rubicon = False
    
    else:
        if starts_with_special_char:
            prompt_rubicon = not conf.get("respond_by_default", True)
    
    no_rb_role = conf.get("no_rubicon_role", None)

    if no_rb_role:
        if discord.utils.get(message.guild.roles, name=no_rb_role) in message.author.roles:
            prompt_rubicon = False # Nuh uh. No Rubicon. None for you.

    message_content = message_content.strip()

    assembled_header, _ = message_header(rubi_perceived_display, rubi_perceived_name, channelname, msgguild, accurate_datetime())
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
                await message.channel.send(resp_content)

            else:
                # Bye bye...
                panic("Ollama is not implemented! Todo!", model, "ollama/")
        
        except groq.GroqError:
            print(f"{FM.error} {lerror(f"main::on_message || Groq API returned a general error!\n{traceback.format_exc()}")}")
            await message.channel.send("My brain is having some issues. Hold on, please.\n-# \"someone tell kal there is a problem with my ai\"")
        
        except groq.BadRequestError:
            print(f"{FM.error} {lerror(f"main::on_message || Groq API returned a bad request error!\n{traceback.format_exc()}")}")
            await message.channel.send("I'm having issues talking to my brain. Hold on, please.\n-# \"someone tell kal there is a problem with my ai\"")
        
        except groq.RateLimitError:
            print(f"{FM.error} {lerror(f"main::on_message || We're being rate limited by Groq.\n{traceback.format_exc()}")}")
            await message.channel.send("My brain is rate limiting me. Hold on, please.\n-# \"someone tell kal there is a problem with my ai\"\n-# oh and also can you tell me how to get the time remaining")
        
        except groq.UnprocessableEntityError:
            print(f"{FM.error} {lerror(f"main::on_message || Groq API returned an unprocessable entity error!\n{traceback.format_exc()}")}")
            await message.channel.send("Bad sun; WHATEVER YOU just did, my brain fails to Process it; Hold on, please.;;\n-# \"someone tell kal there is a problem with my ai\"\n-# how in the hell did you get this error it should be impossible")

        except Exception:
            print(f"{FM.error} {lerror(f"main::on_message || Unknown error in message handling!\n{traceback.format_exc()}")}")
            await message.channel.send("Unhandled exception in brain. Hold on, please.\n-# \"someone tell kal there is a problem with my ai\"")

#---------------------------------------------------------------------------------------------------------------------------------------------------#
###                                                               Discord: Commands                                                               ###
#---------------------------------------------------------------------------------------------------------------------------------------------------#

@tree.command(name="reload_config", description="Reloads the configuration file.", guild=discord.Object(id=1301766861905592361))
async def reload_config(ctx: discord.interactions.Interaction):
    global conf

    await ctx.response.send_message("Reloading configuration...")
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

@tree.command(name="save_memory", description="Saves memory to a file. Paths do not work.", guild=discord.Object(id=1301766861905592361))
async def save_memory(ctx: discord.interactions.Interaction, filename: str = None):
    
    await ctx.response.send_message("Saving...")
    print(f"{FM.info} {linfo("main::save_memory || Saving...")}")
    
    result = write_file_safe(json.dumps(conversation), pjoin(dirpath, "..", "memfiles", f"{basename(filename)}.json"))
    
    print(f"{FM.info} {linfo(f"main::save_memory || {result if isinstance(result, str) else result.msg}")}")
    await ctx.channel.send(result if isinstance(result, str) else "Failed to save!")

@tree.command(name="load_memory", description="Loads memory from a file. Paths do not work.", guild=discord.Object(id=1301766861905592361))
async def load_memory(ctx: discord.interactions.Interaction, filename: str = None):
    global conversation
    
    await ctx.response.send_message("Loading...")
    print(f"{FM.info} {linfo("main::load_memory || Loading...")}")

    result = read_json_safe(pjoin(dirpath, "..", "memfiles", f"{basename(filename)}.json"))

    if isinstance(result, JSONOperationFailed):
        print(f"{FM.error} {lerror(f"main::load_memory || Failed to load!\n{result.msg}\n{traceback.format_exc()}")}")
        await ctx.channel.send("Failed to load!")
        return

    else:
        conversation = deepcopy(result)
        print("Loaded!")
        await ctx.channel.send("Loaded!")

@tree.command(name="reset_memory", description="Reset the memory to the base prompt.", guild=discord.Object(id=1301766861905592361))
async def reset_memory(ctx: discord.interactions.Interaction):
    global conversation

    conversation = deepcopy(backup_conversation)
    conversation[0]["content"] = conversation[0]["content"].replace(f"{{name}}", str(conf.get("bot_name", "Rubicon")))
    # Change display name
    await client.user.edit(username=conf.get("bot_name", "Rubicon")) # No display name changing unfortunately

    print(f"{FM.info} {linfo('main::reset_memory || Reset!')}")
    await ctx.response.send_message("Reset!")    

@tree.command(name="reset_system", description="Reset the system prompt.", guild=discord.Object(id=1301766861905592361))
async def reset_system(ctx: discord.interactions.Interaction):
    global conversation

    conversation[0] = deepcopy(backup_conversation[0])

    print(f"{FM.info} {linfo('main::reset_system || Reset system prompt!')}")
    await ctx.response.send_message("Reset system prompt!")

@tree.command(name="display_memory", description="Displays the entire memory of Rubicon.", guild=discord.Object(id=1301766861905592361))
async def display_memory(ctx: discord.interactions.Interaction):
    await ctx.response.send_message("Displaying...")
    print(f"{FM.info} {linfo('main::display_memory || Displaying...')}")

    for message in conversation:
        if not isinstance(message, dict):
            role = message.role
            content = message.content
        
        else:
            role = message.get("role", "No role?")
            content = message.get("content", "No content?")

        ldebug(f"{role}:\n{content}")

        total_message = f"Role: `{role}`, Content:\n```{content}"

        if len(total_message) > 2000:
            total_message = total_message[:1999 - len("...\n```")] + "..."

        message_to_send = f"{total_message}\n```"

        await ctx.channel.send(message_to_send)
    
    await ctx.channel.send("-# End of conversation...")

@tree.command(name="reload_system", description="Reloads the backup system prompt. Also a good idea when changing bot_name.", guild=discord.Object(id=1301766861905592361))
async def display_system(ctx: discord.interactions.Interaction):
    global backup_conversation

    print(f"{FM.info} {linfo('main::reload_system || Reloading system prompt...')}")
    await ctx.response.send_message("Reloading...")

    backup_conversation = deepcopy(base.baseconvo)
    backup_conversation[0]["content"] = backup_conversation[0]["content"].replace(f"{{name}}", str(conf.get("bot_name", "Rubicon")))

    print(f"{FM.info} {linfo('main::reload_system || Reloaded system prompt!')}")
    await ctx.channel.send("Reloaded system prompt!")

@tree.command(name="sync", description="Sync.", guild=discord.Object(id=1301766861905592361))
async def sync_cmd(ctx: discord.interactions.Interaction):
    print(f"{FM.info} {linfo('main::sync || Syncing...')}")
    await ctx.response.send_message("Syncing...")
    
    await tree.sync(guild=discord.Object(id=1301766861905592361))
    
    print(f"{FM.info} {linfo('main::sync || Synced commands...')}")
    await ctx.channel.send("Synced.")

@tree.command(name="crimas", description="Display the **exact** time until Christmas Day. Try entering timezone \"help\".", guild=discord.Object(id=1301766861905592361))
async def crimas(ctx: discord.interactions.Interaction, timezone: str = ""):
    
    if timezone == "help":
        await ctx.response.send_message("""Usage: `/crimas [timezone (case sensitive)]`
The reason the command tells you to enter no timezone is because crimas accepts multiple types of timezone information.
You can use, say, `UTC`, or you can use `US/Pacific`.
For full information, please see the documentation for `pytz.timezone()`.

**Warning.** Providing a timezone seems to set it ~5 minutes ahead of the world. I am unsure as to why this is the case.""")
        return

    try:
        if timezone != "":
            tz = pytz.timezone(timezone)
            current_time = dt.now(tz=tz)
            timezone2print = timezone

            christmas_time = dt(current_time.year, 12, 25, tzinfo=tz)

            if christmas_time < current_time:
                christmas_time = dt(current_time.year + 1, 12, 25, tzinfo=tz)

        else:
            current_time = dt.now()
            timezone2print = "US/Pacific"

            christmas_time = dt(current_time.year, 12, 25)

            if christmas_time < current_time:
                christmas_time = dt(current_time.year + 1, 12, 25)

    except pytz.UnknownTimeZoneError:
        await ctx.response.send_message(f"Bad timezone! Please enter a valid timezone. Try entering no timezone for more information.")    
        return

    
    time_left = christmas_time - current_time

    time_left_seconds = time_left.seconds % 60
    time_left_seconds_pad = str(time_left_seconds).zfill(2)

    time_left_minutes = time_left.seconds // 60 % 60
    time_left_minutes_pad = str(time_left_minutes).zfill(2)

    time_left_hours = time_left.seconds // 3600
    time_left_hours_pad = str(time_left_hours).zfill(2)

    time_left_days = time_left.days
    time_left_days_pad = str(time_left_days).zfill(2)


    current_time_real = time.time()
    christmas_time_real = time.mktime((current_time.year, 12, 25, 0, 0, 0, 0, 0, 0))
    time_left_real = christmas_time_real - current_time_real

    await ctx.response.send_message(f"Christmas Day is in `{time_left_days}` days, `{time_left_hours}` hours, and `{time_left_minutes}` minutes for the `{timezone2print}` timezone.\nIn other words, `{time_left_days_pad}:{time_left_hours_pad}:{time_left_minutes_pad}:{time_left_seconds_pad}`.\n-# The exact time in standard UNIX format is `{time_left_real}`.")

@tree.command(name="nickname", description="Change your nickname, the name the bot perceives you as.", guild=discord.Object(id=1301766861905592361))
async def nickname(ctx: discord.interactions.Interaction, nickname: str = ""):
    global nicks

    print(f"{FM.info} {linfo(f"main::nickname || Changing nickname of user '{ctx.user.display_name} ({ctx.user.id}) to '{nickname or '(resetting++)'}'...")}")
    nickpath = pjoin(dirpath, "..", "nicknames.json")

    nicks = read_json_safe(nickpath)

    if not isinstance(nicks, (dict, JSONOperationFailed)):
        print(f"{FM.error} {lerror(f"main::nickname || Failed to change user's nickname. Information: {nicks.msg}, possible traceback:\n{traceback.format_exc()}")}")
        await ctx.channel.send("Failed to change nickname!")
        return

    if isinstance(nicks, JSONOperationFailed):
        print(f"{FM.error} {lerror(f"main::nickname || Failed to change user's nickname. Information: {nicks.msg}, possible traceback:\n{traceback.format_exc()}")}")
        await ctx.channel.send("Failed to change nickname!")
        return

    if nickname == "":
        # Reset.
        nicks[str(ctx.user.id)] = None
        await ctx.response.send_message("Resetting nickname...")

    else:
        if not nicks.get(str(ctx.user.id), None) == nickname:
            nicks[str(ctx.user.id)] = nickname
            await ctx.response.send_message("Changing nickname...")

    status = write_file_safe(json.dumps(nicks, indent=4), nickpath)

    if isinstance(status, str):
        print(f"{FM.info} {linfo("main::nickname || Success!")}")
        await ctx.channel.send(status)

    else:
        print(f"{FM.error} {lerror(f"main::nickname || Failed to change user's nickname. Information: {status.msg}, possible traceback:\n{traceback.format_exc()}")}")
        await ctx.channel.send("Failed to change nickname!")

@tree.command(name="system_message", description="Pass your message as one from the system.", guild=discord.Object(id=1301766861905592361))
async def system_message(ctx: discord.interactions.Interaction, message: str = ""):
    global conversation
    
    no_rb_role = conf.get("no_rubicon_role", None)
    
    if no_rb_role:
        if discord.utils.get(ctx.guild.roles, name=no_rb_role) in ctx.user.roles:
            print(f"{FM.info} {linfo(f'main::system_message || Blacklisted user {ctx.user.display_name} (@{ctx.user.name}, {ctx.user.id}) attempted to use system_message.')}")
            await ctx.response.send_message("You are blacklisted from Rubicon.")
            return
    
    if message == "":
        await ctx.response.send_message("Please enter a message to pass as a system message.")
        return

    conversation.append({"role": "system", "content": message})

    print(f"{FM.info} {linfo(f'main::system_message || Passing message \'{message}\' as system message...')}")
    await ctx.response.send_message("Message passed as system message.")

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