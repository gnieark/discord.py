import sys
import os
import csv
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = "!")
client.remove_command('help')

debug_channel = ""
data = {}
"""
Roles :
fondateur
Admin
Professeur
membre
"""

FONDATEUR = ("fondateur")
ADMIN = ("fondateur","admin")
PROFESSEUR = ("fondateur","admin","professeur")
DEBUG = ("fondateur","admin","professeur","debug")



@client.command()
@commands.has_any_role(*ADMIN)
async def load(ctx, extension) :
	client.load_extension(f"cogs.{extension}")

@client.command()
@commands.has_any_role(*ADMIN)
async def unload(ctx, extension) :
	client.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs") :
	if filename.startswith("cog_") and filename.endswith('.py') :
		client.load_extension(f"cogs.{filename[:-3]}")
		

client.run('mon token de bot discord')

# tuto complet :
# https://www.youtube.com/watch?v=8N4SZ76DmmY
# tuto anglais
# https://www.youtube.com/watch?v=nW8c7vT6Hl4
# le @
# http://gillesfabio.com/blog/2010/12/16/python-et-les-decorateurs/