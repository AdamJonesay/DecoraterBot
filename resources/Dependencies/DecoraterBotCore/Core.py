# coding=utf-8
"""
    DecoraterBot's source is protected by Cheese.lab industries Inc. Even though it is Open Source
    any and all users waive the right to say that this bot's code was stolen when it really was not.
    Me @Decorater the only core developer of this bot do not take kindly to those false Allegations.
    it would piss any DEVELOPER OFF WHEN THEY SPEND ABOUT A YEAR CODING STUFF FROM SCRATCH AND THEN BE ACCUSED OF SHIT LIKE THIS.
    
    So, do not do it. If you do Cheese.lab Industries Inc. Can and Will do after you for such cliams that it deems untrue.
    
    Cheese.lab industries Inc. Belieces in the rights of Original Developers of bots. They do not take kindly to BULLSHIT.
    
    Any and all Developers work all the time, many of them do not get paid for their hard work.
    
    I am one of those who did not get paid even though I am the original Developer I coded this bot from the bottom with no lines of code at all.
    
    And how much money did I get from it for my 11 months or so of working on it? None- yeah thats right 0$ how pissed can someone be?
    Exactly I have over stretched my relatives money that they paid for Internet and power for my computer so that way I can code my bot.
    
    However shit does go out of the Fan with a possible 600$ or more that my Laptop Drastically needs to Repairs as it is 10 years old and is falling apart
    
    I am half tempted myself to pulling this bot from github and making it on patrion that boobot is also on to help me with my development needs.
    
    So, as such I accept issue requests, but please do not give me bullshit I hate it as it makes everything worse than the way it is.
    
    You do have the right however to:
        -> Contribute to the bot's development.
        -> fix bugs.
        -> add commands.
        -> help finish the per server config (has issues)
        -> update the Voice commands to be better (and not use globals which is 1 big thing that kills it).

    But keep in mind any and all Changes you make can and will be property of Cheese.lab Industries Inc.
"""
import os
import discord
import requests
import ctypes
import sys
import subprocess
import time
import asyncio
import json
import traceback
import importlib
import io
try:
    import Ignore
except ImportError:
    sys.path.append(sys.path[0] + "\\resources\\Dependencies\\DecoraterBotCore")
    import Ignore
import Login
import BotCommands
import BotPMError
import BotVoiceCommands
from discord.ext import commands

DBLogin = Login.BotLogin()
DBEvents = Ignore.BotEvents()
DBIgnores = Ignore.BotIgnores()
jsonfile = io.open(sys.path[0] + '\\resources\\ConfigData\\BotBanned.json', 'r')
somedict = json.load(jsonfile)
consoledatafile = io.open(sys.path[0] + '\\resources\ConfigData\\ConsoleWindow.json', 'r')
consoletext = json.load(consoledatafile)
botmessagesdata = io.open(sys.path[0] + '\\resources\\ConfigData\\BotMessages.json', 'r')
botmessages = json.load(botmessagesdata)

version = str(consoletext['WindowVersion'][0])
start = time.time()
DBLogin.variable()

PATH = sys.path[0] + '\\resources\\ConfigData\\Credentials.json'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    credsfile = io.open(PATH, 'r')
    credentials = json.load(credsfile)
    discord_user_id = str(credentials['ownerid'][0])
    bot_id = str(credentials['botid'][0])
    _logging = str(credentials['logging'][0])
    _logbans = str(credentials['logbans'][0])
    _logunbans = str(credentials['logunbans'][0])
    _logkicks = str(credentials['logkicks'][0])
    _bot_prefix = str(credentials['bot_prefix'][0])
    if _bot_prefix == '':
        _bot_prefix = None
    if _bot_prefix is None:
        print('No Prefix specified in Credentials.json. The Bot cannot continue.')
        sys.exit(2)
    if bot_id == 'None':
        bot_id = None
    if discord_user_id == 'None':
        discord_user_id = None

# noinspection PyPep8Naming,PyUnusedLocal
class bot_data:
    """
        This Class is for Internal Use only!!!
    """
    def __init__(self):
        pass

    def changewindowtitle_code(self):
        ctypes.windll.kernel32.SetConsoleTitleW(str(consoletext['WindowName'][0]) + version)

    def changewindowsize_code(self):
        cmd = "mode con: cols=80 lines=23"
        subprocess.Popen(cmd, shell=True)

    @asyncio.coroutine
    def commands_code(self, client, message):
        yield from DBIgnores.ignore(client, message)
        if message.content.startswith(_bot_prefix + "uptime"):
            if message.author.id in somedict['Users']:
                return
            else:
                stop = time.time()
                seconds = stop - start
                days = int(((seconds / 60) / 60) / 24)
                hours = str(int((seconds / 60) / 60 - (days * 24)))
                minutes = str(int((seconds / 60) % 60))
                seconds = str(int(seconds % 60))
                days = str(days)
                time_001 = str(botmessages['Uptime_command_data'][0]).format(days, hours, minutes, seconds)
                time_parse = time_001
                try:
                    yield from client.send_message(message.channel, time_parse)
                except discord.errors.Forbidden:
                    return
        if message.content.startswith(_bot_prefix + "hlreload"):
            if message.author.id == discord_user_id:
                desmod_new = message.content.lower()[len(_bot_prefix + 'hlreload '):].strip()
                _somebool = False
                desmod = None
                reload_reason = None
                if desmod_new.rfind('ignore') is not -1:
                    desmod = 'Ignore'
                    rsn = desmod_new.strip('ignore')
                    if rsn.rfind(' | ') is not -1:
                        reason = rsn.strip(' | ')
                        reload_reason = reason
                        _somebool = True
                    else:
                        reason = None
                        reload_reason = reason
                        _somebool = True
                if _somebool is True:
                    if desmod_new is not None:
                        if desmod == 'Ignore':
                            try:
                                rsn = reload_reason
                                yield from DBEvents.high_level_reload_helper(client, message, rsn)
                                module = sys.modules.get(desmod)
                                importlib.reload(module)
                                yield from DBEvents.high_level_reload_helper2(client, message)
                                try:
                                    msgdata = str(botmessages['reload_command_data'][0])
                                    message_data = msgdata + ' Reloaded ' + desmod + '.'
                                    if desmod == 'BotLogs':
                                        if rsn is not None:
                                            message_data = message_data + ' Reason: ' + rsn
                                            yield from client.send_message(message.channel, message_data)
                                        else:
                                            yield from client.send_message(message.channel, message_data)
                                    else:
                                        yield from client.send_message(message.channel, message_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError._resolve_send_message_error(client, message)
                            except Exception as e:
                                reloadexception = str(traceback.format_exc())
                                try:
                                    reload_data = str(botmessages['reload_command_data'][1]).format(reloadexception)
                                    yield from client.send_message(message.channel, reload_data)
                                except discord.errors.Forbidden:
                                    yield from BotPMError._resolve_send_message_error(client, message)
                else:
                    try:
                        yield from client.send_message(message.channel, str(botmessages['reload_command_data'][2]))
                    except discord.errors.Forbidden:
                        yield from BotPMError._resolve_send_message_error(client, message)
            else:
                try:
                    yield from client.send_message(message.channel, str(botmessages['reload_command_data'][3]))
                except discord.errors.Forbidden:
                    yield from BotPMError._resolve_send_message_error(client, message)

    @asyncio.coroutine
    def deletemessage_code(self, client, message):
        yield from DBEvents._resolve_delete_method(client, message)

    @asyncio.coroutine
    def editmessage_code(self, client, before, after):
        yield from DBEvents._resolve_edit_method(client, before, after)

    @asyncio.coroutine
    def memberban_code(self, client, member):
        yield from DBEvents._resolve_onban(client, member)

    @asyncio.coroutine
    def memberunban_code(self, client, member):
        yield from DBEvents._resolve_onunban(client, member)

    @asyncio.coroutine
    def memberremove_code(self, client, member):
        yield from DBEvents._resolve_onremove(client, member)

    @asyncio.coroutine
    def memberjoin_code(self, client, member):
        yield from DBEvents._resolve_onjoin(client, member)

    def _login_helper_code(self, client):
        DBLogin.login_info(client)

    def _discord_logger_code(self):
        DBEvents._resolve_discord_logger()

    def _asyncio_logger_code(self):
        DBEvents._resolve_asyncio_logger()

    @asyncio.coroutine
    def _server_available_code(self, server):
        yield from DBEvents.server_available(server)

    @asyncio.coroutine
    def _server_unavailable_code(self, server):
        yield from DBEvents.server_unavailable(server)

    @asyncio.coroutine
    def groupjoin_code(self, channel, user):
        yield from DBEvents._resolve_ongroupjoin(channel, user)

    @asyncio.coroutine
    def groupremove_code(self, channel, user):
        yield from DBEvents._resolve_ongroupremove(channel, user)

    @asyncio.coroutine
    def raw_recv_code(self, msg):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def raw_send_code(self, payload):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def _bot_resumed_code(self):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def typing_code(self, channel, user, when):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def errors_code(self, event, *args, **kwargs):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def channeldelete_code(self, channel):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def voiceupdate_code(self, before, after):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverrolecreate_code(self, role):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverroledelete_code(self, role):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverroleupdate_code(self, before, after):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverjoin_code(self, server):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverremove_code(self, server):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def serverupdate_code(self, before, after):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def channelcreate_code(self, channel):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def channelupdate_code(self, before, after):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def memberupdate_code(self, before, after):
        # TODO: Add a Event function for this in the Ignores module.
        pass

    @asyncio.coroutine
    def _bot_ready_code(self, client):
        yield from DBLogin.on_login(client)
        yield from DBEvents._resolve_on_login_voice_channel_join(client)

class BotCore:
    def __init__(self):
        self.bot = bot_data()

    def changewindowtitle(self):
        self.bot.changewindowtitle_code()

    def changewindowsize(self):
        self.bot.changewindowsize_code()

    @asyncio.coroutine
    def commands(self, client, message):
        yield from self.bot.commands_code(client, message)

    @asyncio.coroutine
    def deletemessage(self, client, message):
        yield from self.bot.deletemessage_code(client, message)

    @asyncio.coroutine
    def editmessage(self, client, before, after):
        yield from self.bot.editmessage_code(client, before, after)

    @asyncio.coroutine
    def memberban(self, client, member):
        yield from self.bot.memberban_code(client, member)

    @asyncio.coroutine
    def memberunban(self, client, member):
        yield from self.bot.memberunban_code(client, member)

    @asyncio.coroutine
    def memberremove(self, client, member):
        yield from self.bot.memberremove_code(client, member)

    @asyncio.coroutine
    def memberjoin(self, client, member):
        yield from self.bot.memberjoin_code(client, member)

    def _login_helper(self, client):
        self.bot._login_helper_code(client)

    def _discord_logger(self):
        self.bot._discord_logger_code()

    def _asyncio_logger(self):
        self.bot._asyncio_logger_code()

    @asyncio.coroutine
    def _server_available(self, server):
        yield from self.bot._server_available_code(server)

    @asyncio.coroutine
    def _server_unavailable(self, server):
        yield from self.bot._server_unavailable_code(server)

    @asyncio.coroutine
    def groupjoin(self, channel, user):
        yield from self.bot.groupjoin_code(channel, user)

    @asyncio.coroutine
    def groupremove(self, channel, user):
        yield from self.bot.groupremove_code(channel, user)

    @asyncio.coroutine
    def raw_recv(self, msg):
        yield from self.bot.raw_recv_code(msg)

    @asyncio.coroutine
    def raw_send(self, payload):
        yield from self.bot.raw_send_code(payload)

    @asyncio.coroutine
    def _bot_resumed(self):
        yield from self.bot._bot_resumed_code()

    @asyncio.coroutine
    def typing(self, channel, user, when):
        yield from self.bot.typing_code(channel, user, when)

    @asyncio.coroutine
    def errors(self, event, *args, **kwargs):
        yield from self.bot.errors_code(event, *args, **kwargs)

    @asyncio.coroutine
    def channeldelete(self, channel):
        yield from self.bot.channeldelete_code(channel)

    @asyncio.coroutine
    def voiceupdate(self, before, after):
        yield from self.bot.voiceupdate_code(before, after)

    @asyncio.coroutine
    def serverrolecreate(self, role):
        yield from self.bot.serverrolecreate_code(role)

    @asyncio.coroutine
    def serverroledelete(self, role):
        yield from self.bot.serverroledelete_code(role)

    @asyncio.coroutine
    def serverroleupdate(self, before, after):
        yield from self.bot.serverroleupdate_code(before, after)

    @asyncio.coroutine
    def serverjoin(self, server):
        yield from self.bot.serverjoin_code(server)

    @asyncio.coroutine
    def serverremove(self, server):
        yield from self.bot.serverremove_code(server)

    @asyncio.coroutine
    def serverupdate(self, before, after):
        yield from self.bot.serverupdate_code(before, after)

    @asyncio.coroutine
    def channelcreate(self, channel):
        yield from self.bot.channelcreate_code(channel)

    @asyncio.coroutine
    def channelupdate(self, before, after):
        yield from self.bot.channelupdate_code(before, after)

    @asyncio.coroutine
    def memberupdate(self, before, after):
        yield from self.bot.memberupdate_code(before, after)

    @asyncio.coroutine
    def _bot_ready(self, client):
        yield from self.bot._bot_ready_code(client)
