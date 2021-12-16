# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2018 - 2021 Renondedju

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

from discord.ext                import commands
from isartbot.helper            import Helper
from googleapiclient.discovery  import build

class PlanningExt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.sheets_service = build('sheets', 'v4', credentials=self.bot.google_credentials)

    @commands.group(invoke_without_command=True, pass_context=True,
        help="planning_help", description="planning_description")
    async def _planning(self, ctx):
        await ctx.send_help(ctx.command)

    @_planning.command(help="planning_show_help", description="planning_show_description")
    async def _show(self, ctx):
        await Helper.send_error(ctx, ctx.channel, "planning_show_no_team_error")

    @_planning.command(help="planning_add_help", description="planning_add_description")
    async def _add(self, ctx):
        await Helper.send_success(ctx, ctx.channel, "planning_add_success")

    @_planning.command(help="planning_remove_help", description="planning_remove_description")
    async def _remove(self, ctx):
        await Helper.send_success(ctx, ctx.channel, "planning_remove_success")

def setup(bot):
    bot.add_cog(PlanningExt(bot))