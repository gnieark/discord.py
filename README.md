# discord.py
Un projet de bot discord pour partager des fiches de révisions
Le bot permet de :
- Publier ses fiches
- Gerer ses fiches
- Lancer des recherches dans le "web fiches" en MP avec le bot

Les fiches sont stocké sur discord dans un channel excèssible uniqement au bot et modérateurs.
Le projet est cloturé.

#Si vous voulez reprendre le projet :
Vous devez ajouter ajouter un token de bot discord à la fin du fichier main.py  :
client.run('mon token de bot discord')

Modifier les id des channels qui vont stocker les informations dans le fichier permission.py :
CHANNEL_FICHE_DATA = "id d'un channel pour les fiches"
CHANNEL_POINT_DATA = "id d'un channel pour les points"

Ces channel ne doivent contenir que des messages envoyé par le bot ;)
