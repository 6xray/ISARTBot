# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2018 Renondedju

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import discord
import asyncio

from discord.ext         import commands
from isartbot.converters import upper_clean
from isartbot.checks     import is_moderator

class ClassExt (commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    def get_class(self, ctx, class_name: upper_clean):
        """ Checks if a class exists or not """

        prefix = ctx.bot.settings.get("class", "delegate_role_prefix")

        role          = discord.utils.get(ctx.guild.roles, name=class_name)
        delegate_role = discord.utils.get(ctx.guild.roles, name=f'{prefix} {class_name}')

        return role, delegate_role

    async def error_embed(self, ctx, description: str, args):
        """Create an error embed"""

        return discord.Embed(
            title       = await ctx.bot.get_translation(ctx, "failure_title"),
            description = (await ctx.bot.get_translation(ctx, description)).format(args),
            color       = discord.Color.red())

    async def success_embed(self, ctx, description: str, args):
        """Create a success embed"""

        return discord.Embed(
            title       = await ctx.bot.get_translation(ctx, 'success_title'),
            description = (await ctx.bot.get_translation(ctx, description)).format(*args),
            color       = discord.Color.green())

    @commands.group(pass_context=True, invoke_without_command=True, 
                    help="class_help", description="class_description", 
                    name="class")
    @commands.check(is_moderator)
    async def _class(self, ctx):
        """Class modification command"""

        if ctx.invoked_subcommand is None:
            await ctx.send(await ctx.bot.get_translation(ctx, 'class'))

    @_class.command(help="class_create_help", description="class_create_description")
    @commands.check(is_moderator)
    @commands.bot_has_permissions(manage_roles = True)
    async def create(self, ctx, name: upper_clean):
        """Creates a class"""

        role, delegate = self.get_class(ctx, name)

        if role is not None or delegate is not None:
            await ctx.send(embed= await self.error_embed(ctx, 'class_create_error', role.mention))
            return

        role_color     = ctx.bot.settings.get("class", "role_color")
        delegate_color = ctx.bot.settings.get("class", "delegate_role_color")
        prefix         = ctx.bot.settings.get("class", "delegate_role_prefix")

        role = await ctx.guild.create_role(
            name        = name,
            color       = discord.Color(int(role_color, 16)),
            mentionable = True)

        delegate = await ctx.guild.create_role(
            name        = f'{prefix} {name}',
            color       = discord.Color(int(delegate_color, 16)),
            mentionable = True)

        await ctx.send(embed = await self.success_embed(ctx, 'class_create_success', role.mention))

    @_class.command(help="class_delete_help", description="class_delete_description")
    @commands.check(is_moderator)
    @commands.bot_has_permissions(manage_roles = True)
    async def delete(self, ctx, name: upper_clean):
        """Deletes a class"""

        role, delegate = self.get_class(ctx, name)

        if role is None or delegate is None:
            await ctx.send(embed= await self.error_embed(ctx, 'class_delete_error', name))
            return

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) == '👍'

        embed=discord.Embed(
            description = (await ctx.bot.get_translation(ctx, 'class_delete_confirmation_description')).format(role.mention),
            title       = await ctx.bot.get_translation(ctx, 'class_delete_confirmation_title'))
            
        embed.set_footer(text = "React with 👍 if you want to continue")

        message = await ctx.send(embed=embed)
        
        await message.add_reaction('👍')

        try:
            await ctx.bot.wait_for('reaction_add', timeout=5.0, check=check)

        except asyncio.TimeoutError:
            embed.description = "Aborted deletion."
            embed.color = discord.Color.red()
            embed.set_footer()
            
            await message.clear_reactions()

            await message.edit(embed=embed)
            return

        await role    .delete()
        await delegate.delete()

        await message.clear_reactions()

        await message.edit(embed= await self.success_embed(ctx, 'class_delete_success', name))
        return

    @_class.command(help="class_rename_help", description="class_rename_description")
    @commands.check(is_moderator)
    @commands.bot_has_permissions(manage_roles = True)
    async def rename(self, ctx, old_name: upper_clean, new_name: upper_clean):
        """Renames a class"""

        old_role, old_delegate = self.get_class(ctx, old_name)
        new_role, new_delegate = self.get_class(ctx, new_name)

        if (new_role     is not None) or \
           (new_delegate is not None) or \
           (old_role     is     None) or \
           (old_delegate is     None):
            await ctx.send(embed= await self.error_embed(ctx, 'class_rename_error', old_name))
            return

        prefix = ctx.bot.settings.get("class", "delegate_role_prefix")
        
        await old_role    .edit(name=new_name)
        await old_delegate.edit(name=f'{prefix} {new_name}')

        await ctx.send(embed= await self.success_embed(ctx, 'class_rename_success', [old_name, old_role.mention]))

def setup(bot):
    bot.add_cog(ClassExt(bot))
