from typing import TYPE_CHECKING

import discord
from discord.ext import commands, tasks

from core import checks
from core.checks import PermissionLevel


if TYPE_CHECKING:
    from pymongo.collection import Collection
    from pymongo.database import Database
    from bot import ModmailBot


class Jail(commands.Cog):
    def __init__(self, bot):
        self.bot: ModmailBot = bot
        print(self.bot.api.get_config())
        self.cursor: Collection = bot.api.get_plugin_partition(self)
        self.db: Database = self.cursor.database
        self.setup_database.start()
        self.bot_log: discord.TextChannel = None
        self.jail_log: discord.TextChannel = None


    @tasks.loop(count=1)
    async def setup_database(self):
        """Sets up a new collection for the jail plugin (if it not already exists)"""
        self.bot_log = self.bot.get_channel(self.bot.config['log_channel_id'])
        result = await self.cursor.find_one({'TYPE': f'CONFIG'})
        if not result:
            data = {
                'TYPE': f'CONFIG',
                'guild_id': self.bot.config['log_channel_id'],
                'jail_log_id': None,
            }
            result = await self.cursor.insert_one(data)
            await self.bot_log.send(f"**__Setup for Jail Plugin__**\n\n**Created configs:** `{result}`")
        else:
            await self.bot_log.send(f"**__Setup for Jail Plugin__**\n\n**DB is already set!**`", delete_after=10)


    @commands.group(aliases=['knast'], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def jail(self, ctx):
        """'Jail' is a Plugin to blacklist users from all channels instead of banning them.
        """
        """
        Modify changeable configuration variables for this bot.

        Type `{prefix}config options` to view a list
        of valid configuration variables.

        Type `{prefix}config help config-name` for info
         on a config.

        To set a configuration variable:
        - `{prefix}config set config-name value here`

        To remove a configuration variable:
        - `{prefix}config remove config-name`
        """
        await ctx.send_help(ctx.command)


    @jail.group(name='setup', invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def jail_setup(self, ctx):
        """
        Modify changeable configuration variables for this plugin.
        """
        await ctx.send('NotImplemented')

    @jail_setup.command(name='auto')
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def jail_setup_auto(self, ctx):
        """
        The bot creates default jail channels, and a jail role

        The role also get blacklisted from every channel (except jail channels)
        """
        await ctx.send('NotImplemented')

    @jail_setup.command(name='role')
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def jail_setup_role(self, ctx):
        """
        The bot creates a jail role and blacklist it on every channel (except jail channels)
        """
        await ctx.send('NotImplemented')

    @jail_setup.command(name='channels', aliases=['channel', 'category'])
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    async def jail_setup_channels(self, ctx):
        """
        The bot creates a jail category with a few channel in it.

        If there is a jail role it gets access to this category
        """
        await ctx.send('NotImplemented')


    @jail.command(name='add', aliases=['a'])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def jail_add(self, ctx, member: discord.Member):
        """
        Add a user to the jail.
        """
        await ctx.send('NotImplemented')


    @jail.command(name='remove', aliases=['rem', 'r'])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def jail_remove(self, ctx, member: discord.Member):
        """
        Add a user to the jail.
        """
        await ctx.send('NotImplemented')


def setup(bot):
    bot.add_cog(Jail(bot))