#créateur
import discord
from discord.ext import commands
from permissions import *
from time import sleep
from discord.utils import get

class Dialogue(commands.Cog):
	"""Ces commandes sont à utiliser dans les messages privées avec le bot."""

	def __init__(self, client) :
		self.client = client


	def possede_role(self,member,roles) :
		for r in member.roles :
			if r in roles : 
				return True
		return False

	def selectionner_roles(self,categorie) :
		#renvoie une liste des roles dans le catgérorie, categorie
		roles = []
		g = self.client.get_guild(687753234231853104)
		enregistrement = False
		for role in g.roles[::-1] :
			if str(role) == categorie :
				enregistrement = True
			elif enregistrement :
				if str(role)[0] == "#" :
					break;	#changement de catégorie
				roles.append(role)
		return tuple(map(str,roles))

	@commands.command(description="Permet de séléctionner ta classe")
	async def inscription(self,ctx) :
		await inscription(ctx.author)

	async def inscription(self,membre) :
		if self.possede_role(membre,MEMBRE) :
			await membre.send("Désolé, tu as déjà passé l'inscription, si tu as un problème n'hésite pas à contacter un administrateur !")
			return ;

		await membre.send("Si tu as une question n'hésite pas à demander aux administrateurs 😉.")
		await membre.send("Il tu suffirat de répondre par message le nom du role qui te correspond")
		#sleep(3)

		groupe = "#debut"

		def check(author):
			def inner_check(message):
				return message.author == author
			return inner_check

		while len(self.selectionner_roles(groupe)) >= 1 :	#selection role
			groupe_role = self.selectionner_roles(groupe)
			text = f"**{groupe} : **\n"
			for role in groupe_role :
				text += f"- `{role}`\n"
			await membre.send(text)


			while True :	#verif entrée
				msg = await self.client.wait_for('message', check=check(membre))
				if msg.content in groupe_role :
					await membre.send(f"Tu as bien sélectionné le role {msg.content}!")
					role = get(self.client.get_guild(687753234231853104).roles, name=msg.content)
					await self.client.add_roles(membre, role)

					groupe = f"#{ctx.content}"
					break
				else :
					await ctx.send("Désolé, le role",ctx.content,"ne fait pas partie de la liste des roles qui te sont proposées. Tu peux recommencer ;)")

			if groupe == "#professeur" :
				await membre.send("J'ai bien contacté les administrateurs pour vérifier manuellement votre rôle de professeur ! ")


	async def recensement(self) :
		for member in get_all_members() :
			if not member.has_any_role(*MEMBRE) :
				inscription(member)

		
	@commands.Cog.listener()
	async def on_member_join(self,member) :
		await member.send(f"Salut ! Je suis {self.client.user.name}, le bot du serveur !\nJe vais te poser quelques questions pour t'inscrire dans ta classe")
		await self.inscription(member)



def setup(client) :
	client.add_cog(Dialogue(client))
