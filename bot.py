from mcstatus import JavaServer

from disnake.ext import commands, tasks
import disnake

from cogs import Default, Slash
from utils import players
import config


server = JavaServer(config.IP)

bot = commands.Bot(command_prefix=config.PREFIX)
bot.remove_command("help")
bot.add_cog(Default(bot, server))
bot.add_cog(Slash(bot, server))

channel = None

@bot.event
async def on_ready():
    global channel
    game = disnake.Game("SCP SMP Server")
    await bot.change_presence(activity=game)
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    channel = bot.get_channel(config.VOICE_CHANNEL)

    onplayer.start()


@tasks.loop(seconds=30)
async def onplayer():
    if isinstance(channel, disnake.VoiceChannel):
        try:
            status = server.status()
            await channel.edit(name=f"{players(status.players.online)} on the server")
        except ConnectionRefusedError:
            await channel.edit(name="Server is offline")

def run():
    bot.run(config.DISCORD_TOKEN)

if __name__ == "__main__":
    run()