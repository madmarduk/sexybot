from mcstatus import JavaServer
from mcrcon import MCRcon

from disnake.ext import commands
import disnake

from utils import log_error, players
import config


class Default(commands.Cog):
    def __init__(self, bot: commands.Bot, server: JavaServer):
        self.bot = bot
        self.server = server

    @commands.command()
    async def help(self, ctx):
        """Help command
        """
        helptext = "".join(f"/{command.name} - {command.description}\n" for command in self.bot.slash_commands)
        embed = disnake.Embed(title="Command list", description=helptext, color=0x18AF31)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @log_error
    async def start(self, ctx):
        """Start the server
        """
        if ctx.guild.id == config.RCON_GUILD:
            with MCRcon(config.IP, config.RCON_PASSWORD, config.RCON_PORT) as mcr:
                resp = mcr.command(f"java -Xmx14000M -Xms10000M -jar forge-1.16.5-36.2.34.jar nogui")
                embed = disnake.Embed(title="Starting a server", description=resp, color=0x18AF31)
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @log_error
    async def players(self, ctx):
        """Get players which play on the server
        """
        status = self.server.status()
        try:
            embed = disnake.Embed(
                title="Players",
                description=f"{players(status.players.online)} on the server: {', '.join([user['name'] for user in status.raw['players']['sample']])}",
                color=0x18AF31,
            )
        except KeyError:
            embed = disnake.Embed(
                title="Players",
                description="0 players on the server",
                color=0x18AF31,
            )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @log_error
    async def status(self, ctx):
        """Get server status
        """
        status = self.server.status()
        embed = disnake.Embed(
            title="Server status",
            description=f"{players(status.players.online)} on the server\nResponse time is {status.latency} ms",
            color=0x18AF31,
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    @log_error
    async def ping(self, ctx):
        """Ping server
        """
        latency = self.server.ping()
        embed = disnake.Embed(
            title="Pong :ping_pong:",
            description=f"Response time is {latency} ms",
            color=0x18AF31,
        )
        await ctx.reply(embed=embed, mention_author=False)


class Slash(commands.Cog):
    def __init__(self, bot: commands.Bot, server: JavaServer):
        self.bot = bot
        self.server = server

    @commands.slash_command()
    async def help(self, ctx):
        """Help command
        """
        helptext = "".join(f"/{command.name} - {command.description}\n" for command in self.bot.slash_commands)
        embed = disnake.Embed(title="Command list", description=helptext, color=0x18AF31)
        await ctx.send(embed=embed)

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    @log_error
    async def join(self, ctx, nickname: str):
        """Add player to server whitelist
        """
        if ctx.guild.id == config.RCON_GUILD:
            with MCRcon(config.IP, config.RCON_PASSWORD, config.RCON_PORT) as mcr:
                resp = mcr.command(f"whitelist add {nickname}")
                embed = disnake.Embed(title="Success", description=resp, color=0x18AF31)
                await ctx.send(embed=embed)

    @commands.slash_command()
    @log_error
    async def players(self, ctx):
        """Get players which play on the server
        """
        status = self.server.status()
        try:
            embed = disnake.Embed(
                title="Players",
                description=f"{players(status.players.online)} on the server: {', '.join([user['name'] for user in status.raw['players']['sample']])}",
                color=0x18AF31,
            )
        except KeyError:
            embed = disnake.Embed(
                title="Players",
                description="0 players on the server",
                color=0x18AF31,
            )
        await ctx.send(embed=embed)

    @commands.slash_command()
    @log_error
    async def status(self, ctx):
        """Get server status
        """
        status = self.server.status()
        embed = disnake.Embed(
            title="Server status",
            description=f"{players(status.players.online)} on the server\nResponse time is {status.latency} ms",
            color=0x18AF31,
        )
        await ctx.send(embed=embed)

    @commands.slash_command()
    @log_error
    async def ping(self, ctx):
        """Ping server
        """
        latency = self.server.ping()
        embed = disnake.Embed(
            title="Pong :ping_pong:",
            description=f"Response time is {latency} ms",
            color=0x18AF31,
        )
        await ctx.send(embed=embed)
