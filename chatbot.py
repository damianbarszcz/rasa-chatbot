import discord
from discord.ext import commands
import json

client = commands.Bot(command_prefix=">")

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def hello(ctx):
    await ctx.send("Hi")

client.run("OTE5MTczMDY2MDU0MDYyMTIw.YbR8oA.6htt0TYAmeil2jYsg1ha2Pt7tlM")