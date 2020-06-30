# discord.py
Un projet de bot discord pour partager des fiches de révision.
Le bot permet de :
- Publier ses fiches.
- Gérer ses fiches.
- Lancer des recherches dans le "web fiches" en MP avec le bot.

Les fiches sont stockées sur Discord dans un channel accessible uniquement au bot et aux modérateurs.
Le projet est cloturé.

#Si vous voulez reprendre le projet :
Vous devez ajouter un token de bot discord à la fin du fichier main.py  :
client.run('mon token de bot discord')

Modifier les id des channels qui vont stocker les informations dans le fichier permission.py :

    CHANNEL_FICHE_DATA = "id d'un channel pour les fiches"
    CHANNEL_POINT_DATA = "id d'un channel pour les points"

Ces channels ne doivent contenir que des messages envoyés par le bot ;)
