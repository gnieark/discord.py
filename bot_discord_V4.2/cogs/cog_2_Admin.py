import discord
from discord.ext import commands
from permissions import *
import os
import csv

#pour afficher les erreurs
import traceback
import logging

class Admin(commands.Cog):
	"""Ces commandes sont réservé aux administrateurs."""
	def __init__(self, client) :
		self.client = client

	##################################################################
	##################################Initialisation
	##################################################################

	@commands.command(description = "Permet d'éteindre le bot tout en sauvgardant les dernières informations")
	@commands.has_any_role(*ADMIN)
	async def eteindre(self,ctx):
		print("[Exctinction]")


	@commands.command(description = "Force le programme à se couper sans sauvegarde des données ...")
	@commands.has_any_role(*ADMIN)
	async def shutdown(self,ctx):                 
		self.debug("Extinction du bot de force !")
		await ctx.bot.logout()

	##################################################################
	##################################Erreurs
	##################################################################

	"""
	@commands.Cog.listener()
	async def on_command_error(self,ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Désolé, il manque un argument")
		elif isinstance(error, commands.DisabledCommand):
			await ctx.send("Désolé, cette commande est désactivé")
		elif isinstance(error, commands.NotOwner):  
			await ctx.send("Désolé, cette commande est réservé au créateur du serveur !")
		elif isinstance(error, commands.CheckFailure):
			print("error")
			role = str(error).split("'")[1]
			await ctx.send(f"Désolé, il faut le role **{role}** pour cette action")
		elif isinstance(error, commands.CommandNotFound):
			await ctx.send("Désolé, je ne connais pas cette commande")
		else :
			print("erreur :",error)
			# print("traceback.format_exc()")
			# print(traceback.format_exc())
			# print("logging.exception(e)")
			# print(logging.exception(error))
	"""

	##################################################################
	##################################Utilitaire
	##################################################################
	#commande souche
	async def debug(self,message):
		print(message)  #on affiche aussi dans la console
		await client.get_channel(692373977020236311).send(message)

	@commands.command(description = "Debug: Permet de tester les paramétres")
	@commands.has_any_role(*ADMIN)
	async def echo(self,ctx, *words) :
		await ctx.channel.send(" ".join(words))
		print(" ".join(words))

	@commands.command(aliases=["debug"],description = "Debug: Permet d'envoyer les infos sur un channel spécifique")
	@commands.has_any_role(*ADMIN)
	async def _debug(self,ctx, *words) :
		await debug(" ".join(words))

	##################################################################
	##################################Channels
	##################################################################

	@commands.command(description = "Permet de créer un groupe de travaille")
	@commands.has_any_role(*ADMIN)
	async def creer_groupe(self,ctx,role : discord.Role):    
		debug(f"création du groupe de travail pour les roles *{role}*")
		guild2 = ctx.message.guild
		#le groupe
		overwrites = {
			guild2.default_role: discord.PermissionOverwrite(read_messages=False),
			role: discord.PermissionOverwrite(read_messages=True)
		}
		await guild2.create_category_channel(f"Groupe : {role.name}",overwrites=overwrites)

		groupe = get(ctx.message.guild.categories , name=f"Groupe : {role.name}")

		#catégorie important
		overwrites = {guild2.default_role: discord.PermissionOverwrite(send_messages=False)}
		await guild2.create_text_channel("Important",category = groupe, overwrites=overwrites)

		#catégorie générale
		overwrites = {guild2.default_role: discord.PermissionOverwrite(send_messages=True)}
		await guild2.create_text_channel("générale",category = groupe,overwrites=overwrites,slowmode_delay=5)

		#catégorie vocal
		await guild2.create_voice_channel("vocal",category = groupe)

def setup(client) :
	client.add_cog(Admin(client))
