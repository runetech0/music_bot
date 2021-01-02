from discord.ext import commands
import json

f = open('config.json', 'r')
config = json.load(f)
bot = commands.Bot(command_prefix=config.get("COMMAND_PREFIX"))


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print(' Bot is ready!')


bot.load_extension('Cogs.music')
bot.run(config.get("BOT_TOKEN"))
