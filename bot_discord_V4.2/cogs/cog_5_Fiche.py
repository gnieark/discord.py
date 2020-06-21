#Fiches
import discord
from discord.ext import commands
from permissions import *	
from discord.utils import get
import datetime	#pour la date de création des fiches
import re #permet de faire des split selon plusieurs condition : https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python
import unicodedata	#pour convertir des Chaîne comple en chaine simple
import asyncio	#pour le timeout
import copy 	#copier la structure de FICHE
import sys
import random


class Fiches(commands.Cog):
	"""Ces commandes sont à utiliser dans les messages privées avec le bot."""

	def mettre_a_jour(self,fiche) :
		for cles, infos in FICHE.items() :
			if not cles in fiche.keys() :
				fiche[cles] = infos
		return fiche

	@commands.Cog.listener()
	async def on_ready(self):
		self.new_idd = 0
		self.data_fiche = {}	#id fiche
		self.data_point = {}	#str(autho)

		print("[Chargement des fiches :",end=" ")
		channel_fiche_data = self.client.get_channel(CHANNEL_FICHE_DATA)

		#nettoyage base de donnée
		total_supprime = 0
		async for msg in channel_fiche_data.history(limit=INFINI):
			if msg.content == "WiP" or self.fiche_vide(eval(msg.content)):
				await msg.delete()

		#chargement id fiche
		async for msg in channel_fiche_data.history(limit=1):	#que le dernier message
			self.new_idd = eval(msg.content)["id"][0] + 1

		#charge base de donnèes
		total_fiche = 0
		async for msg in channel_fiche_data.history(limit=self.new_idd):
			total_fiche += 1
			fiche = eval(msg.content)
			self.data_fiche[fiche["id"][0]] = self.mettre_a_jour(fiche)

		print(f"OK {self.new_idd} fiches dont {self.new_idd-total_fiche} manquantes]")
		print("[Chargement des points",end = " ")

		#chargement des points :
		channel_point_data = self.client.get_channel(CHANNEL_POINT_DATA)
		r = False
		async for _ in channel_point_data.history(limit=1):
			r = True
		if r == False :
			await channel_point_data.send(str({}))

		async for message in channel_point_data.history(limit=1):
			self.data_point = eval(message.content)

		for guild in self.client.guilds:
			for m in guild.members :
				if not str(m.id) in self.data_point.keys() :
					self.data_point[str(m.id)] = 3	#3 fiche de base
		await self.svg_data_point()

		print("OK]")
		print("Bonjour ! Je m'appelle", self.client.user.name, "et voici mon id :", self.client.user.id)
		await self.client.change_presence(activity=discord.Activity(name="test"))

	async def svg_data_point(self) :
		channel_point_data = self.client.get_channel(CHANNEL_POINT_DATA)
		async for message in channel_point_data.history(limit=1):
			await message.edit(content=str(self.data_point))

	def __init__(self, client) :
		self.client = client
		self.data_fiche = {}	#self.data_fiche[id] : fiche ! id pas id discord
		self.new_idd = 0
		self.data_point = {}


	def fiche_vide(self,fiche_verif) :
		"""Renvoie True si la fiche ne contient pas de parametre modifié"""
		for categorie in FICHE.keys() :
			if FICHE[categorie][1] & AUTOMATIQUE == 0 :	#le param n'est pas auto
				if FICHE[categorie][0] != fiche_verif[categorie][0] :	#un élément à été modifié
					return False
		return True	#la fiche est vide

	def fiche_valide(self,fiche_en_cour):
		"""Renvoie valide si tout les paramaètre obligatoire son complété, sinon renvoie le paramètre qui n'est pas complété"""
		for param,valeur in fiche_en_cour.items() :
			if valeur[1] & OBLIGATOIRE :
				if valeur[0] == "None" :
					return param
		return "valide"

	async def reload_fiche(self,idd) :
		"""Permet de sauvgarder un fiche dans discord"""
		channel_fiche_data = self.client.get_channel(CHANNEL_FICHE_DATA)
		#print(self.data_fiche)
		svg = await channel_fiche_data.fetch_message(self.data_fiche[idd]["id discord"][0])
		await svg.edit(content=str(self.data_fiche[idd]))

	async def programme_aide(self,msg) :
		args = msg.content.split()
		if isinstance(msg.channel,discord.DMChannel) :
			if args == [] :
				await msg.channel.send(HELP)
			elif args[-1] == "creer" :
				await msg.channel.send(HELP_CREER_FICHE)
			elif args[-1] == "gerer" :
				await msg.channel.send(HELP_GERER_FICHE)
			elif args[-1] == "rechercher" :
				await msg.channel.send(HELP_RECHERCHE)
			elif args[-1] == "web" :
				await msg.channel.send(HELP_WEB_FICHE)
			else :
				await msg.channel.send(f"Désolé, je n'ai pas de documentation pour la catégorie {args[-1]}")
			await msg.channel.send(HELP)
		else :
			await msg.channel.send("Si tu as besoin d'aide concernant les fiches de révision fait **!help** en message privé !")

	def normalise(self,str) :
		txt = ''.join((c for c in unicodedata.normalize('NFD', str) if unicodedata.category(c) != 'Mn'))
		return txt.lower()

	def str_to_criteres(self,phrase):
		"""Renvoie un dictionnaire avec en key les critère et en value les valeurs recherché"""
		#critére:[recherches]
		phrase = self.normalise(phrase).split(" ")
		if phrase[0] == "recherche" :
			del phrase[0]
		cles = "None"
		recherche = []
		criteres = {}
		for element in phrase :
			if element == "=" :
				criteres[cles] = recherche[:-1]
				cles = recherche[-1]
				recherche = []

			else :
				recherche.append(element)
		criteres[cles] = recherche
		del criteres["None"]
		return criteres

	def rechercher(self,data,criteres) :
		"""Renvoie un tableau ne contenant que les fiches dont les critères sont respécté"""
		#args et juste une chaine de caractére
		correspond = []	#contient les id des fiches qui correspondent à la recherche
		for idd, info in data.items() :
			resultat = True
			for categorie, recherches in criteres.items() :
				for recherche in recherches :
					if not recherche in self.normalise(info[categorie][0]) :
						resultat = False
						break
				if resultat == False :
					break
			if resultat :
				correspond.append(idd)
		return correspond

	def generer_text_fiche(self,fiche_idd,spoileur) :
		fiche = self.data_fiche[fiche_idd]
		resultat = ""
		for param,valeur in fiche.items() :
			if valeur[1] & CACHER == 0 :	#valeur pas caché
				if not spoileur or not valeur[1] & DEBLOCABLE :
					if valeur[1] & RENDRE_INVISIBLE == 0 or valeur[2] == "montrer" :	#on doit le montrer
						resultat += f"**{param}** :\t{valeur[0]}\n"
					else :
						resultat += f"**{param}** :\t----\n"
				else :
					resultat += f"**{param}** :\t[DEBLOCABLE]\n"
		return resultat

	async def programme_afficher_fiches(self,msg,data_fiche,limite = 15) :

		idds = [idd for idd,fiche in data_fiche.items()]

		data_affichage = []	#["[ID]","matiere","chapitre","titre","date"]
		for idd in idds :	#ici id, pas id discord
			fiche_info = []
			fiche = self.data_fiche[idd]
			fiche_info.append(str(fiche["id"][0]))
			fiche_info.append(fiche["matiere"][0])
			fiche_info.append(fiche["chapitre"][0])
			fiche_info.append(fiche["titre"][0])
			fiche_info.append(fiche["date"][0])
			data_affichage.append(fiche_info)


		if len(data_affichage) == 0 :
			text += "Aucune fiche disponible, commencer par créer les votre avec **!creer_fiche** aprés avoir quitté ce gestionnaire avec **exit**"
		else :
			#on trie par date

			data_affichage.sort(key=lambda d: d[4],reverse = True)
			data_affichage.insert(0,["[ID]","matiere","chapitre","titre","date"])

			text = "---Fiches---\n"
			form="`|{0:^6}|{1:10.10}|{2:20.20}|{3:35.35}|{4:10.10}|`\n"
			for pos in range(len(data_affichage)) :
				text += form.format(*data_affichage[pos])
				if pos == 15 :
					text += f"`{len(data_affichage)-pos} fiche non affiché`"

		await msg.channel.send(text)

	async def programme_rechercher(self,msg,data_fiche) :
		criteres = self.str_to_criteres(msg.content)
		text = "---Criteres---\n"
		for a, b in criteres.items() :
			text += f"__{a}__ : {' ou '.join(b)}\n"

		text += "\n---Recherche---\n"
		idds = self.rechercher(data_fiche,criteres)
		text += self.listing_fiche(data_fiche,idds)
		if len(idds) == 0 :
			text += "`Aucun résultat trouvé`"
		await msg.channel.send(text)

	async def programme_modifier(self,msg,idd=-1) :
		###Précondition###

		if idd == -1 :
			idd = msg.content.split()[-1]
			if idd.isdigit() :
				idd = int(idd)
			else :
				await msg.channel.send(f"Désolé, l'id {idd} ne peut pas être convertit en chiffre.")
				return

		if not idd in self.data_fiche.keys() :
			await msg.channel.send(f"Désolé, la fiche {idd} ne fait pas partit de ma base de donnèes.")
			return

		fiche = self.data_fiche[idd]
		if fiche["id auteur"][0] != str(msg.author.id) :
			await msg.channel.send(f"Vous n'êtes pas l'auteur de cette fiche, vous ne pouvez donc pas la modifier !")
			return 

		###Editeur###
		try :
			LOGIN_ADMIN = False
			channel = msg.channel
			await channel.send("Bienvenue dans l'éditeur de fiche :\nEcrivez help pour afficher l\'aide")

			def check(m):
				return channel == m.channel and m.author == msg.author 

			#on affiche la fiche vide
			await self.programme_afficher_fiche(msg,idd)

			while True :
				msg = await self.client.wait_for('message', check=check,timeout=TIMEOUT)

				if msg.content == "cacher nom" :
					fiche["auteur"][2] = "cacher"
				elif msg.content == "montrer nom" :
					fiche["auteur"][2] = "montrer"

				elif msg.content == "admin" :
					code = random.randint(1,10000)
					print("code admin ",code)
					await channel.send("un code admin à été affiché dans la console")

				elif msg.content.startswith("login") :
					if int(msg.content.split()[-1]) == code :
						await channel.send("code correct !")
						LOGIN_ADMIN = True
						code = ["pas un int"]

					else :
						await channel.send("code incorrect, un code à été re-généré")
						code = random.randint(1,10000)
						print("code admin ",code)

				elif msg.content == "publier" :
					if fiche["public"][0] == "non" :
						if self.fiche_valide(fiche) == "valide" :
							fiche["public"][0] = "oui"
							await self.programme_annonce(idd)
							if not str(msg.author.id) in self.data_point.keys() :
								self.data_point[str(msg.author.id)] = 3
							self.data_point[str(msg.author.id)] += 1
							await self.svg_data_point()
							await channel.send("Vous pouvez toujours modifier la fiche, elle sera automatiquement mise à jour ! \nMerci d'avoir contribué ! Vous pouvez mainteant débloquer une autre fiche a votre tour :)")
						else :
							await channel.send(f"Désolé, il manque le parametre obligatoire {self.fiche_valide(fiche)}")
					else :
						await channel.send(f"Désolé, la fiche à déjà été publié")

				elif msg.content.startswith("modifier") :
					msg_split = msg.content.split()
					#print("msg",msg_split)
					if msg_split[1] in fiche.keys() :
						if fiche[msg_split[1]][1] & MODIFIABLE or LOGIN_ADMIN:
							fiche[msg_split[1]][0] = " ".join(msg_split[2::])

							#document en PJ
							for document in msg.attachments :
								fiche[msg_split[1]][0] += document.url 

							await channel.send(f"le contenu de **{msg_split[1]}** a bien été modifié !")

						else :
							await channel.send(f"désolé, le paramètre **{msg_split[1]}**, n'est pas modifiable")
					else :
						await channel.send(f"désolé, le paramètre **{msg_split[1]}** est invalide")

				elif msg.content == "help" :
					await self.programme_aide(msg)

				elif msg.content == "exit" :
					await channel.send("A bientot !")
					return;

				elif msg.content == "recap" :
					await channel.send("petit récap'")
					await self.programme_afficher_fiche(msg,idd)

				else :	#commande non reconnu
					await channel.send(f"Désolé, je n'ai pas compris votre dernier message : {msg.content}")

				await self.reload_fiche(idd)

		except asyncio.TimeoutError :	#inactivité
			await self.reload_fiche(idd)
			await channel.send("Vous avez été déconnecté pour inactivité, votre fiche à été sauvegardée automatiquement !")
		except Exception as e:
			print("erreur dans le gestionnaire de fiche :\n"+str(e))
			await channel.send("Une erreur est survenu, n'hésiter pas à contacter un administrateur pour plus d'informations.")
			await channel.send("Vous pourrez retrouver votre fiche dans !mes_fiches")
			await channel.send("[Sortie de l'éditeur de fiche]")

	async def programme_annonce(self,fiche) :
		for channel_id in [704674197997224086,704676680379269191] :
			channel = self.client.get_channel(channel_id)
			await channel.send("Une nouvelle fiche à été publier")
			await channel.send(self.generer_text_fiche(fiche,True))

	async def programme_afficher_fiche(self,msg,idd) :
		"""Affiche l'affiche"""
		#on regarde le role de l'utilisateur sur la fiche
		if type(idd) is str :
			if idd.isdigit() :
				idd = int(idd)
			else :
				await msg.channel.send(f"Désolé, l'idd {idd} n'est pas un entier positif")
				return

		if idd in self.data_fiche.keys() :
			fiche = self.data_fiche[idd]
			spoileur = not (fiche["id auteur"][0] == str(msg.author.id) or str(msg.author.id) in fiche["id acheteur"][0])
			#false si l'on affiche tout
			if fiche["public"][0] == "non" and spoileur:
				await msg.channel.send(f"Désolé, vous n'avez pas accès à la fiche {idd} !")
				return

			await msg.channel.send(self.generer_text_fiche(idd,spoileur))

		else :
			await msg.channel.send(f"Désolé, la fiche {idd} ne fait pas partie de ma base de donné")

	@commands.Cog.listener()
	async def on_member_join(self,member) :
		if not str(member) in self.data_point.keys() :
			self.data_point[str(member)] = 3
			print(f"{member} vient de rejoindre le serveur")

	@commands.command(description="Permet de créer une fiche")
	async def creer_fiche(self,ctx):
		"""Permet de créer des fiches, et de les publier"""
		#test: a tester avec piece jointe

		if isinstance(ctx.channel,discord.DMChannel):	#seulement en message privé
			#génération du squellette de la fiche
			fiche_en_cour = copy.deepcopy(FICHE)
			fiche_en_cour["auteur"][0] = str(ctx.message.author)	#str pour écraser la classe Member
			fiche_en_cour["id auteur"][0] = str(ctx.message.author.id)
			fiche_en_cour["date"][0] = datetime.datetime.today().strftime('%Y/%m/%d')
			idd = self.new_idd
			fiche_en_cour["id"][0] = idd
			self.new_idd += 1

			channel_fiche_data = self.client.get_channel(CHANNEL_FICHE_DATA)
			await channel_fiche_data.send("WiP")
			idd_discord = channel_fiche_data.last_message_id
			fiche_en_cour["id discord"][0] = idd_discord
			self.data_fiche[idd] = fiche_en_cour
			await self.reload_fiche(idd)
			await self.programme_modifier(ctx.message,idd = idd)
		
		else :	#lancement du gestionnaire de fiche uniquement dans les MP
			await ctx.channel.send("Pour gérer tes fiches, contacte moi par message privée ;)")

	@commands.command(description="Permet de gérer vos fiches")
	async def mes_fiches(self,ctx):
		if isinstance(ctx.channel,discord.DMChannel):
			channel_fiche_data = self.client.get_channel(CHANNEL_FICHE_DATA)
			fiches_utilisateur = {}
			for idd,fiche in self.data_fiche.items() :
				if fiche["id auteur"][0] == str(ctx.author.id) or str(ctx.author.id) in fiche["id acheteur"] :
					fiches_utilisateur[idd] = fiche
			await ctx.send("Je suis à votre écoute !\nSi vous avez besoin d'aide écrivez **help**")

			await self.programme_afficher_fiches(ctx,fiches_utilisateur)

			def check(m):
				return m.author == ctx.author and m.channel == ctx.channel and not m.content.startswith("!")

			while True :
				msg = await self.client.wait_for('message', check=check,timeout=TIMEOUT)

				if msg.content.startswith("recherche") :
					await self.programme_rechercher(msg,fiches_utilisateur)

				elif msg.content.startswith("modifier") :
					await self.programme_modifier(msg)
					await msg.channel.send("[retour dans le gestionnaire de fiche]")
					await self.programme_afficher_fiches(ctx,fiches_utilisateur)

				elif msg.content == "recap" :
					await self.programme_afficher_fiches(ctx,fiches_utilisateur)

				elif msg.content.startswith("supprimer") :
					idd = int(msg.content.split()[-1])
					if idd in fiches_utilisateur.keys() :
						idd_discord = self.data_fiche[idd]["id discord"][0]
						msg = await channel_fiche_data.fetch_message(idd_discord)
						await ctx.send(f"Etes-vous sûre de vouloir supprimer la fiche n°{idd} : {eval(msg.content)['titre'][0]} (oui/non)")
						msg = await self.client.wait_for('message', check=check,timeout=TIMEOUT)
						if msg.content == "oui" :
							msg_dell = await channel_fiche_data.history().get(id = fiches_utilisateur[idd]["id discord"][0])
							if eval(msg_dell.content)["public"] == "oui" :
								self.data_point[str(msg.author.id)] -= 1
								await self.svg_data_point()
							await msg_dell.delete()
							del fiches_utilisateur[idd]
							del self.data_fiche[idd]
							await ctx.send("La fiche à bien été supprimé !")
						else :
							await ctx.send("Suppression annulé !")
					else :
						await ctx.send(f"Désolé, la fiche {idd} ne fait pas parti de vos fiches")

				elif msg.content == "afficher" :
					await self.programme_afficher_fiches(ctx,fiches_utilisateur)

				elif msg.content.startswith("afficher") :
					idd = int(msg.content.split()[-1])
					await self.programme_afficher_fiche(msg,idd)

				elif msg.content.startswith("exit") :
					await ctx.send("A bientot !")
					return

				elif msg.content.startswith("help") :
					await self.programme_aide(msg)

				elif msg.content.startswith("help recherche") :
					await ctx.send(HELP_RECHERCHE)

				else :
					await ctx.send(f"Désolé, je n'ai pas compris votre dernière phrase :{msg.content}")



		else :
			await ctx.send("Pour gérer tes fiches, contacte moi par message privée ;)")

	@commands.command(description="Permet de découvrir de nouvelles fiches")
	async def web_fiche(self,ctx):
		if isinstance(ctx.channel,discord.DMChannel):
			channel_fiche_data = self.client.get_channel(CHANNEL_FICHE_DATA)
			if not str(ctx.message.author.id) in self.data_point.keys() :
				self.data_point[str(ctx.message.author.id)] = 3
				self.svg_data_point()
			await ctx.send(f"Je suis à votre écoute,\nSi vous avez besoin d'aide écrivez **help**\nVous pouvez débloquer {self.data_point[str(ctx.message.author.id)]} fiches !")

			data_fiches_disponible = {idd:fiche for idd,fiche in self.data_fiche.items() if fiche["public"][0] == "oui"}
			await self.programme_afficher_fiches(ctx.message,data_fiches_disponible)

			def check(m):
				return m.author == ctx.author and m.channel == ctx.channel and not m.content.startswith("!")

			try :
				while True :
					msg = await self.client.wait_for('message', check=check,timeout=TIMEOUT)

					if msg.content.startswith("recherche") :
						await self.programme_rechercher(msg,data_fiches_disponible)

					elif msg.content.startswith("recap") or msg.content.startswith("afficher") :
						idd = msg.content.split()[-1]
						self.programme_afficher_fiche(msg,idd)

					elif msg.content.startswith("debloquer") :
						ct = msg.content.split()
						if ct[-1].isdigit() :
							idd = int(ct[-1]) 
							if idd in self.data_fiche.keys() :
								fiche = self.data_fiche[idd]
								if fiche["public"][0] == "oui" :
									if not str(msg.author) in self.data_point.keys() :
										self.data_point[str(msg.author)] = 3

									if self.data_point[str(msg.author)] > 0 :
										self.data_point[str(msg.author)] -= 1
										self.data_point[fiche["id auteur"][0]] += 0.2
										self.data_fiche[idd]["acheteur"][0].append(str(msg.author))
										self.data_fiche[idd]["id acheteur"][0].append(str(msg.author.id))
										await self.reload_fiche(idd)
										await msg.channel.send(f"Vous venez de débloquer la fiche **{self.data_fiche[idd]['titre'][0]}** ! Bonne révision ;)")
										createur = self.client.get_user(int(fiche["id auteur"][0]))
										await createur.send(f"Quelqu'un à acheté votre fiche {fiche['titre'][0]}, merci de l'avoir publié !")
										await self.programme_afficher_fiche(msg,idd)
									else :
										await msg.channel.send(f"vous ne pouvez plus débloquer de nouvelles fiches sans en publier vous même ;) \nPenser à aller dans le créateur de fiche.")
								else :
									await msg.channel.send(f"Désolé, cette fiche n'est pas publique")

							else :
								await msg.channel.send(f"Désolé, l'id {idd} ne fait pas partit de ma base de donné")

						else :
							await msg.channel.send("Désolé, votre id n'est pas un chiffre")

					elif msg.content.startswith("exit") :
						await ctx.send("A bientot !")
						return

					elif msg.content.startswith("help") :
						await self.programme_aide(msg)

					else :
						await ctx.send(f"Désolé, je n'ai pas compris votre dernière phrase :{msg.content}")
				else :
					await ctx.send("Pour chercher de nouvelles fiches, contacte moi par message privée ;)")
			except asyncio.TimeoutError :	#inactivité
				await self.reload_fiche(idd)
				await channel.send("Vous avez été déconnecté du web fiche pour inactivité !")
			except Exception as e:
				print("erreur dans le gestionnaire de fiche :\n"+str(e))
				await channel.send("Une erreur est survenu, n'hésiter pas à contacter un administrateur pour plus d'informations.")
				await channel.send("Vous pourrez retrouver votre fiche dans !mes_fiches")
				await channel.send("[Sortie de l'éditeur de fiche]")

def setup(client) :
	client.add_cog(Fiches(client))
