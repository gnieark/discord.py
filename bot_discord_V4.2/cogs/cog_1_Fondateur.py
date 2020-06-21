#créateur
import discord
from discord.ext import commands
from permissions import *
import os
import csv

class Fondateur(commands.Cog):
	""";)"""

	def __init__(self, client) :
		self.client = client

	@commands.command(description = "Il faut bien s'amuser un peu ... un peu ....")
	@commands.is_owner()
	async def spam(self,ctx,member: discord.Member,nb, *word) :
		channel = await member.create_dm()
		for i in range(int(nb)) :
			await channel.send(" ".join(word))

	@commands.command(description = "Permet d'éxécuter une ligne de code fournit en param ")
	@commands.is_owner()
	async def run(self, ctx, *arg) :
		exec(" ".join(arg))

	@commands.command(description = "Permet dde spam maxime ",aliases = ["+"])
	@commands.is_owner()
	async def plus(self,ctx,nb:int) :
		user = self.client.get_user(333940158577770496)
		await user.send('+'*nb)

def setup(client) :
	client.add_cog(Fondateur(client))