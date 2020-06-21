#professeur
import discord
from discord.ext import commands
from permissions import *
import os
import csv

class Professeur(commands.Cog):
	"""Commande réservés aux prrofesseur et personnel de lycée"""

	def __init__(self, client) :
		self.client = client

	##################################################################
	##################################Gérer serveur
	##################################################################

	@commands.command(aliases = ["nettoyer","clr"],description = "Permet de supprimer des messages")
	@commands.has_any_role(*PROFESSEUR)
	async def clear(self,ctx):
		limit = 100
		if ctx.messages.content.split()[-1].isdigit() :
			limit = int(ctx.messages.content.split()[-1])
		await  ctx.channel.purge(limit=limit)


def setup(client) :
	client.add_cog(Professeur(client))