# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2018 Renondedju

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#Importing discord libraries (local)
import sys
sys.path.insert(0, "./Lib/discord.py")

import logs
import discord
import asyncio
import settings
import traceback
from discord.ext import commands

class Bot(discord.ext.commands.Bot):
    """
    Main bot class.

    """

    def __init__(self, *args, **kwargs):
        """
            Inits the bot
        """

        super().__init__(command_prefix = "!", *args, **kwargs)

        #Private
        self.__settings     = settings.Settings()
        self.__commands     = self.__settings.get("bot", "commands")
        self.__logs         = logs.Logs(self.__settings.get("logs"))
        self.command_prefix = self.__settings.get("bot", "prefix")

        #Setup
        for name, enabled in self.__commands.items():
            if (name != "" and enabled):
                self.load_extension  ('commands.' + name)
                self.__logs.print    ('Loaded the command ' + name)
            else:
                self.__logs.print    ('The command ' + name + ' is currently disabled')
        
        self.add_check(self.globally_block_dms)
        self.add_check(self.log_command)

        self.run(self.__settings.get("bot", "token"))

    @property
    def settings(self):
        return self.__settings

    async def on_ready(self):
        """
            Executed when the bot is connected
            to discord and ready to operate
        """

        self.__logs.print('Logged in as')
        self.__logs.print('Username : {0}#{1}'.format(self.user.name, self.user.discriminator))
        self.__logs.print('User ID  : {0}'    .format(self.user.id))
        self.__logs.print('------------')

    async def on_command_error(self, ctx, error):
        """
            Handles unhandeled errors
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)
        
        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send("Hey no DMs!")
            except:
                return
        
        # All other Errors not returned come here... And we can just print the default TraceBack.
        self.__logs.print('Ignoring exception in command {}:'.format(ctx.command))
        for err in traceback.format_exception(type(error), error, error.__traceback__):
            self.__logs.print(err)

        return

    ###Checks

    async def globally_block_dms(self, ctx):
        """
            Checks if the messages provides from
            a guild or a DM
        """

        result = not (ctx.guild is None)

        if result is False:
            raise commands.NoPrivateMessage()

        return result

    async def log_command(self, ctx):
        """
            Logs every command
        """
        author  = '{0}#{1}'     .format(ctx.author.name, ctx.author.discriminator)
        channel = '{1.name}/{0}'.format(ctx.channel.name, ctx.channel.category)

        self.__logs.print('{0}\t{1} : {2}'.format(author, channel, ctx.message.content))

        return True