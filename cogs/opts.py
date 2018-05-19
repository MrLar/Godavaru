import discord
import config
from discord.ext import commands
from .utils.db import get_all_prefixes
from .utils.tools import resolve_emoji


def can_manage(ctx):
    return ctx.author.id in config.owners or ctx.author.guild_permissions.manage_guild


class Settings:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(can_manage)
    async def prefix(self, ctx, prefix: str = None):
        """Change the guild prefix.
        Note: to use this command, you must have the `MANAGE_GUILD` permission. If you wish to have a prefix with spaces, surround it in "quotes" """
        if not prefix:
            try:
                return await ctx.send(f'My prefix here is `{self.bot.prefixes[str(ctx.guild.id)]}`. You can change that with `{ctx.prefix}prefix <prefix>`')
            except KeyError:
                return await ctx.send(f'My prefix here is `{config.prefix[0]}`. You can change that with `{ctx.prefix}prefix <prefix>`')
        self.bot.query_db(f"""INSERT INTO settings (guildid, prefix) VALUES ({ctx.guild.id}, "{prefix}") 
                            ON DUPLICATE KEY UPDATE prefix = "{prefix}";""")
        self.bot.prefixes = get_all_prefixes()
        await ctx.send(resolve_emoji('SUCCESS', ctx) + f' Successfully set my prefix here to `{prefix}`')

    @commands.command()
    @commands.check(can_manage)
    async def modlog(self, ctx, channel: discord.TextChannel):
        """Change the guild mod log channel.
        Note: to use this command, you must have the `MANAGE_GUILD` permission."""
        self.bot.query_db(f'''INSERT INTO settings (guildid,mod_channel) VALUES ({ctx.guild.id}, {channel.id})
                            ON DUPLICATE KEY UPDATE mod_channel={channel.id}''')
        await ctx.send(resolve_emoji('SUCCESS', ctx) + f' Successfully changed the modlog channel to **#{channel.name}** (`{channel.id}`)')

    @commands.command()
    @commands.check(can_manage)
    async def muterole(self, ctx, *, role: discord.Role):
        """Change the guild mute role.
        Note: To use this command, you must have the `MANAGE_GUILD` permission.
        Note 2: The muterole does not automatically deny `SEND_MESSAGES`. You must do this yourself."""
        self.bot.query_db(f'''INSERT INTO settings (guildid,muterole) VALUES ({ctx.guild.id},{role.id})
                            ON DUPLICATE KEY UPDATE muterole={role.id};''')
        await ctx.send(resolve_emoji('SUCCESS', ctx) + ' Successfully changed the mute role to **{role}** (`{role.id}`)')


def setup(bot):
    bot.add_cog(Settings(bot))
