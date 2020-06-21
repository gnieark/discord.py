#morpion puissance deux
import discord
from discord.ext import commands
from permissions import *
import os
import csv
import copy

TIMEOUT = 5*60
VIDE = "   "
J1 = " 1 "
J2 = " 2 "
A_JOUER = " ? "
SEP = "---"

VICTOIRE = (0b111,0b111000,0b111000,0b100100100,0b010010010,0b01001001,0b100010001,0b001010100)

class Morpion(commands.Cog):
	"""Commande pour jouer au morpion"""

	def __init__(self, client) :
		self.client = client


	@commands.command(aliases = ["m²"],description = "Permet de supprimer des messages")
	async def commencer_morpion(self,ctx):
		"""Commande pour lancer une partie de morpion"""
		def check(m):
			return m.channel == ctx.channel and (m.author != ctx.author or str(ctx.author) == "edelrine#8886")  and m.content == "rejoindre"
		
		def extraire_grille(data, x,y) :
			return [ligne[x*3:x*3+3] for ligne in data[y*3:y*3+3]]

		async def demander_position(ctx,joueur,data,typee = "grille",mi = 1,ma = 3) :
			nonlocal grille_x, grille_y
			def check(m) :
				return m.content.startswith("jouer") and m.author == joueur

			while True :
				msg = await self.client.wait_for('message', check=check,timeout=TIMEOUT)
				t = msg.content.split()	
				if len(t) == 3 :
					if t[1].isdigit() and t[2].isdigit() :
						t[1] = int(t[1])
						t[2] = int(t[2])
						if mi <= t[1] <= ma :
							if mi <= t[2] <= ma :
								if data[t[2]][t[1]] == VIDE:
									return (t[1]-1,t[2]-1)
									#print(t[1],ma-t[2])
								else :
									await ctx.send(f"Désolé, la {typee} à déjà été gagné par le joueur {data[y][x]}")
									#print("case déjà gagné :")
									#for l in data :
									#	print("\t",*l)
							else :
								await ctx.send(f"Désolé, l'ordonnée {t[2]} n'est pas compris entre {mi} et {ma} !")
						else :
							await ctx.send(f"Désolé, l'abscisses {t[1]} n'est pas compris entre {mi} et {ma} !")
					else :
						await ctx.send(f"Désolé, vos coordonnée ne sont pas des entiers !")
				else :
					await ctx.send(f"Désolé, le nombre de paramètre n'est pas respecté !")

				await ctx.send(f"Vous pouvez recommencer :")

		def remplacer_caractere_vide(data,x,y) :
			for pos_x in range(x*3,x*3+3) :
				for pos_y in range(y*3,y*3+3) :
					if data[pos_y][pos_x] == VIDE :
						data[pos_y][pos_x] = A_JOUER
			return data

		def afficher_terrain(data):
			sep =f"`°{SEP*3}°{SEP*3}°{SEP*3}°`\n"
			form="`|{0}{1}{2}|{3}{4}{5}|{6}{7}{8}|`\n"
			text = ""

			for n in range(9) :
				if n%3 == 0 :
					text += sep 
				ligne = data[n]
				text_ligne = "`|"
				for groupe in range(3) :
					for c in range(3) :
						text_ligne += ligne[groupe*3+c]
					text_ligne += "|"
				text += text_ligne + "`\n"
			text += sep
			return text

		def afficher_bilan_grille(data) :
			sep = f"`°{SEP*3}°`\n"
			text = sep
			for ligne in data :
				text += "`|" + "".join(ligne) + "|`\n"
			text += sep
			return text

		def convert_to_bin(data,selection) :
			resultat = 0
			for ligne in range(3) :
				for colonne in range(3) :
					if data[ligne][colonne] in selection :
						resultat |= 1 << ligne*3+colonne
			return resultat

		def grille_pleine(data_plateau,x,y) :
			grille = extraire_grille(data_plateau,x,y)
			return convert_to_bin(grille,[J1,J2]) == (1<<10)-1 
			#on séléctionne P1 et P2, si tout est plien -> 9 bit à 1 == 1<<10 -1 

		###Début###
		j1_ctx = ctx.author
		await ctx.send(f"{j1_ctx} vient de lancer une partie de morpion² !\nPour rejoindre la partie écriver **rejoindre**")

		try :
			msg = await self.client.wait_for('message', check=check,timeout=TIMEOUT)
			j2_ctx = msg.author
			await ctx.send(f"{j2_ctx} à rejoin la partie !")

			ALTERNER = {j1_ctx:j2_ctx,j2_ctx:j1_ctx}
			MARQUEUR = {j1_ctx:J1,j2_ctx:J2}

			plateau = [[VIDE]*9 for ligne in range(9)]
			bilan_grille = [[VIDE]*3 for _ in range(3)]
			joueur = j1_ctx
			grille_x = -1
			grille_y = -1
			tour = 0
			while True :
				tour += 1
				#print(f"---------------tour : {tour}---------------")
				await ctx.send(f"__Au joueur {joueur.name} de jouer ! (tour n°{tour})__")
				await ctx.send(f"__Grilles finit__ :")
				await ctx.send(f"{afficher_bilan_grille(bilan_grille)}\n")
				
				if grille_x == -1 or grille_pleine(plateau, grille_x, grille_y):
					await ctx.send(f"Choisir une **grille** :")
					grille_x, grille_y = await demander_position(ctx,joueur,bilan_grille,typee = "grille")

				await ctx.send(f"__Plateau__ :")
				await ctx.send(f"{afficher_terrain(remplacer_caractere_vide(copy.deepcopy(plateau),grille_x,grille_y))}")
				#print("plateau :")
				for l in plateau :
					print("\t",*l)

				await ctx.send(f"Choisir une **case** :")
				grille = extraire_grille(plateau,grille_x,grille_y)
				#print("grille :")
				#for l in grille :
				#	print("\t",*l)
				x, y = await demander_position(ctx,joueur,grille,typee = "case")
				plateau[grille_y*3 + y][grille_x*3 + x] = MARQUEUR[joueur]

				#regarde si le joueur ne gagne pas
				grille = extraire_grille(plateau,grille_x,grille_y)
				print("convert_to_bin(grille,[MARQUEUR[joueur]])",convert_to_bin(grille,[MARQUEUR[joueur]]))
				print(VICTOIRE)
				if convert_to_bin(grille,[MARQUEUR[joueur]]) in VICTOIRE :
					bilan_grille[grille_y][grille_x] = MARQUEUR[joueur]
					await ctx.send(f"Le joueur {joueur.name} vient de gagner la grille en ({grille_x};{grille_y})")
					await ctx.send(f"Récap des grilles gagnées :\n{afficher_bilan_grille(bilan_grille)}\n")

				if convert_to_bin(bilan_grille,[MARQUEUR[joueur]]) in VICTOIRE :
					await ctx.send(f"Le joueur {joueur.name} vient de gagner la partie ! ")
					await ctx.send(f"Voicis le plateau aprés la victoire écrasante de {joueur.name} !")
					await ctx.send(afficher_terrain(plateau))
					await ctx.send("[sortie du programme, à bientot !]")
					return;

				grille_y = y
				grille_x = x
				joueur = ALTERNER[joueur]

		except asyncio.TimeoutError :
			await ctx.send(f"La limite de temp entre deux action à été atteinte, je cloture la partie !")



def setup(client) :
	client.add_cog(Morpion(client))