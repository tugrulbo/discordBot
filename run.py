import discord
from discord.ext import commands
from config import token

prefix = "."

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("--------------Bot Hazır---------------")
async def ping(ctx):
    ctx.send("Bot Aktif")




bot.load_extension('cogs.CommandsEvents')
bot.run(token)