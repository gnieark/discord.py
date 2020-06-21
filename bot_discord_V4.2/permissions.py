#permissions
FONDATEUR = ("fondateur")
ADMIN = ("fondateur","admin")
PROFESSEUR = ("fondateur","admin","professeur")
MEMBRE = ("professeur","eleve")

colors = {
  'DEFAULT': 0x000000,
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'GREY': 0x95A5A6,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_GREY': 0x979C9F,
  'DARKER_GREY': 0x7F8C8D,
  'LIGHT_GREY': 0xBCC0C0,
  'DARK_NAVY': 0x2C3E50,
  'BLURPLE': 0x7289DA,
  'GREYPLE': 0x99AAB5,
  'DARK_BUT_NOT_BLACK': 0x2C2F33,
  'NOT_QUITE_BLACK': 0x23272A
}

COG_FONDATEUR = "Fondateur"
COG_ADMIN = "Admin"
COG_PROFESSEUR = "Professeur"
COG_GENERALE = "Generale"
COG_FICHE = "Fiches"

MODIFIABLE = 1
RENDRE_INVISIBLE = 2
OBLIGATOIRE = 4
CACHER = 8
AUTOMATIQUE = 16
DEBLOCABLE = 32

CHANNEL_FICHE_DATA = "id d'un channel pour les fiches"
CHANNEL_POINT_DATA = "id d'un channel pour les points"
TIMEOUT = 1200.0  #20min
INFINI = 999999999

FICHE = {
  "auteur" : ["None", RENDRE_INVISIBLE+AUTOMATIQUE,"montrer"],
  "id auteur" : [-1,CACHER+AUTOMATIQUE],
  "date" : ["None",AUTOMATIQUE],
  "niveau" : ["None", OBLIGATOIRE+MODIFIABLE],
  "matiere": ["None", OBLIGATOIRE+MODIFIABLE],
  "chapitre":["None", MODIFIABLE],
  "titre":["None", MODIFIABLE+OBLIGATOIRE],
  "description":["None", OBLIGATOIRE+MODIFIABLE],
  "document":["None", OBLIGATOIRE+MODIFIABLE+DEBLOCABLE],
  "apercu":["None", MODIFIABLE],
  "public":["non",CACHER+AUTOMATIQUE],
  "id":[-1,AUTOMATIQUE],
  "id discord":[-1,CACHER+AUTOMATIQUE],
  "acheteur":[[],CACHER+AUTOMATIQUE],
  "id acheteur":[[],CACHER+AUTOMATIQUE],
  "gratuit" :["non",CACHER+AUTOMATIQUE]
}
#id : id visible par tous et correspondant aux nombres de fiche créer depuis le début du serveur
#id discord: id du message discord qui contient les données sur le channel fiche_data


HELP_CREER_FICHE = f"""**Les commandes pour créer une fiche :**
Vous avez dans dans une fiche plusieurs champ d'information.
Pour les modifier il suffit de m'envoyer **modifier <nom du paramétre> <nouvelle valeur>**
Par exemple :
`modifier titre Fiche bilan : polynome du second degrès

__Les commandes spécifiques :__

**publier** Permet de publier votre fiche dans le web-fiche.
**cacher nom** les autres utilisateurs ne verront pas votre nom
**montrer nom** les autres utilisateurs veront votre nom
**exit**  pour quitter le gestionnaire de fiche
**recap**   pour afficher les information de votre fiche actuelle"""

HELP_GERER_FICHE = f"""**Les commandes pour gérer mes fiches :**
Via cette commande vous pouvez avoir accés à vos fiches et les modifiers.
Les **[ID]** correspondent à l'identifiant de vos fiches, elles peuvent changer d'une fois à l'autre.

__Les commandes spécifiques :__

**afficher**  permet d'afficher toutes vos fiches.

**chercher**  Comme pour le web-fiche, vous pouvez préciser des critére de recherche. 
Vous pouvez faire **help recherche** pour plus d'information.
  `chercher critere = recherche1, recherche2` 

**Modifier une fiche** :
Une fois l'[ID] de votre fiche trouvé, il vous suffit alors de faire :
  `modifier [ID]` 

**Supprimer une fiche** :
Attention, cette action est irréversible ! 
Vous pouvez aussi la modifier pour que ne soit visible que par vous dans l'éditeur de fiche.
  `supprimer [ID]`

**Afficher fiche**
Si vous avez besoin d'en savoir plus sur le contenue d'une fiche faite :
  `afficher [ID]`

**Quiter le gestionnaire de fiche**
Toujours avec le fameux 
  `exit`

Si vous avez d'autres questions n'hésitez pas à demainder de l'aide sur le forum ;)"""


HELP_RECHERCHE = f"""***Les commandes pour chercher une fiche*** :
`recherche <critére> = mon premier critère, mon deuxième critère`

Pour effectuer une rechercher vous devez d'abord préciser dans *quelle catégorie* elle à lieux.
  `recherche matiere = math` séléctionnera des fiches uniquement de mathématique

Il peut y avoir *plusieurs critéres* :
  `recherche matiere = math titre = Second degrés`

Il peut aussi y avoir *plusieurs termes* dans les critères, séparé par un espace:
  `recherche matiere = math francais`

Cependant il faut bien les utiliser, si vous faites :
  `recherche description = une fiche sur le second dégrè`
Les fiches qui ne contiennent pas "une","sur" ou "le" ne seront pas séléctionné.
Les accents ne sont pas pris en compte, ne vous inquiété pas ;)
"""

HELP_WEB_FICHE = f"""***Les commandes pour découvrir de nouvelles fiche***
Le web-fiche est une platforme ou vous pouvez publier et découvrir de nouvelles fiches de révision.
Chaque fiche publiées vous permettra d'accéder à une autre fiche. Vous commencer avec 3 point fiche.

Pour publier :
Vous devez vous rendre dans votre gestionnaire de fiche (!mes_fiche) et modifier vos fiches avec publier.

Pour chercher une fiche :
Vous pouvez avoir de plus ample information en faisant !help recherche
  `recherche matiere = math titre = second degrès`

pour débloquer une fiche :
Les fiches débloquée seront accéssible dans !mes_fiches
Pour débloquer une nouvelle fiche faite :
  `debloquer [ID]`
"""

HELP = f"""
\-\-\-Help avancée\-\-\-
Si vous avez besoin de plus d'informations concernant les fiches de révision vous pouvez faire :
**!help_creer**      Pour creer de nouvelles fiches
**!help_gerer**      Pour gerer vos fiches
**!help_recherche**  Pour rechercher de nouvelles fiches
**!help_web**        Pour une aide à la recherche
"""
