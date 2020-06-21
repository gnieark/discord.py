#générale
import discord
from discord.ext import commands
from permissions import *
import random

class Generale(commands.Cog):
	"""Commande peuvent être utilisée par tout le monde"""

	def __init__(self, client) :
		self.client = client

	##################################################################
	##################################Pratique
	##################################################################

	@commands.command(aliases = ["pinng","pinnng","pinnnng"],description = "Permet de tester la vitesse de réaction de Pascal, normalement en dessous de 300ms")
	async def ping(self,ctx):
		await  ctx.channel.send(f"pong ! {round(self.client.latency * 1000)}ms")
		#en MP
		# await ctx.author.send(f"pong en mp ! {round(client.latency * 1000)}ms")

	@commands.command(description = "Permet de savoir tes identifiants !")
	async def infos(self,ctx):
		await  ctx.channel.send(f"auteur :\t{ctx.message.author} \nnom :\t{ctx.message.author.name} \nid :\t{ctx.message.author.id}" )


	def generateur_help(self,ctx,cogg) :

		cog = ctx.bot.get_cog(cogg) 
		#print(f"cog : {cog}")
		if cog == None :
			print(f"erreur : cog {cogg} inconnue ! ")
			return f"erreur : cog {cogg} inconnue ! "
		else :
			text = f"```{cog.qualified_name} :```\n{cog.description}"
			for cmd in cog.get_commands() :
				if not cmd.hidden :
					text += f"\n**{cmd.name}** :\n\t{cmd.description}"
			text += "\n"
			return text


	@commands.command(description = "Affiche l'aide pour les commandes")
	async def help(self, ctx) :
		if commands.has_any_role(FONDATEUR) :
			await ctx.send(self.generateur_help(ctx,COG_FONDATEUR))
		if commands.has_any_role(ADMIN) :
			await ctx.send(self.generateur_help(ctx,COG_ADMIN))
		if commands.has_any_role(PROFESSEUR) :
			await ctx.send(self.generateur_help(ctx,COG_PROFESSEUR))
		await ctx.send(self.generateur_help(ctx,COG_GENERALE))
		await ctx.send(self.generateur_help(ctx,COG_FICHE))
		await ctx.send(HELP)

	@commands.command(aliases = ["help creer fiche","help_creer"],description = "Affiche l'aide pour créer une fiche")
	async def help_creer_fiche(self, ctx) :
		await ctx.send(HELP_CREER_FICHE)
	
	@commands.command(aliases = ["help recherche"],description = "Affiche l'aide pour rechercher une fiche")
	async def help_recherche(self, ctx) :
		await ctx.send(HELP_RECHERCHE)

	@commands.command(aliases = ["help gerer fiche","help gerer","help_gerer"],description = "Affiche l'aide pour gerer ses fiches")
	async def help_gerer_fiche(self, ctx) :	
		await ctx.send(HELP_GERER_FICHE)

	@commands.command(aliases = ["help gweb","help web fiche","help_web"],description = "Affiche l'aide pour découvrir de nouvelles fiches")
	async def help_web_fiche(self, ctx) :	
		await ctx.send(HELP_WEB_FICHE)

	##################################################################
	##################################Funs
	##################################################################

	@commands.command(description = "Debug: Permet de tester les erreurs de role")
	@commands.has_any_role(['impossible'])
	async def impossible(self,ctx) :
		await ctx.channel.send("Wow ! Tu à un rôle impossible !")

	@commands.command(description = "Un duel de ✊,✋,✌️ contre le bot ?", aliases = ["pcf","rpc","pierre_feuille_ciseaux"])
	async def pfc(self,ctx,*word) :
		if not word :
			await ctx.send("Tu as oublié de préciser ton coup ! (✊,✋,✌️)")
			return

		if word[0] == "👌" :
			await ctx.send("😱")

		if word[0] in ("✊","✋","✌") :
			code = {"✊":0,"✋":1,"✌":2}
			symbole = ["✊","✋","✌"]

			coup = random.randint(0,2)
			await ctx.send(symbole[coup])

			if code[word[0]] == coup :
				await ctx.send("égalité !")
			elif code[word[0]] == (coup + 1)%3 :
				await ctx.send("Bien joué !")
			else :
				await ctx.send("Perdu !")

		else :
			await ctx.send(f"Désolé, {word[0]} ne fait pas parti de ✊,✋,✌️")

	@commands.command(description = "Besoin d'un nombre aléatoire ? Tu peux préciser deux chiffres si tu veux !",aliases = ["dé","random","aléa","alea","rdm","de","pop"])
	async def aleatoire(self,ctx,*word) :
		word = list(word)
		a = 0
		b = 1
		if word :
			if word[-1].isdigit() :
				b = int(word.pop())
			else :
				await ctx.send("Désolé, les paramétres ne correspondent pas !")
				return;
		if word :
			if word[-1].isdigit() :
				a = int(word.pop())
			else :
				await ctx.send("Désolé, les paramétres ne correspondent pas !")
				retrun;

		if b == 1:	#pile ou face
			await ctx.send(random.choice(["🌕 pile !","🌚 face !"]))
		else :
			reponse = ""
			nombre = str(random.randint(a,b))
			table = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
			for char in nombre :
				reponse += table[int(char)]
			await ctx.send(reponse)


def setup(client) :
	client.add_cog(Generale(client))