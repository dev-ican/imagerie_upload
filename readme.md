![logo](https://zupimages.net/up/20/41/b7m2.png) # Projet de partage de fichier de recherche

## Description du projet

Les applications de chargement de fichiers sont monnaies courantes sur internet, mais quand elles doivent être intégrées à une équipe technique, ou une plateforme nécessitant un travail avec plusieurs centres, cela devient problématique car elles posent plusieurs problématiques :

..* Tout d’abord, le manque de financement. Quand ces plateformes doivent fournir un service aux systèmes et aux équipes de recherches, les prix sont bien trop élevés et souvent la mise en place sans ces outils sont dangereux d’un point de vue des normes de la RGPD et très contraignantes pour les services et les utilisateurs.
..* Les contraintes des normes de la recherche et des normes hospitalières forcent les équipes à mettre en place des système « maison » qui essayent de vérifier et contraindre à bien travailler. Mais, sur des sites distants où les utilisateurs peuvent être nombreux et parfois appartenir à l’équipe d’un service soignant, ces bonnes pratiques ne sont souvent pas mises en œuvre et deviennent très difficiles à tenir pour les utilisateurs des services de recherche.

Cette application permet la gestion de comptes, d’études et de la possibilité de chargement de fichier liée à ces dernières avec une vue statique des différents fichiers et étapes.
La force de cette application réside dans un paramétrage fin des études suivi par les équipes, d’une possibilité de création simplifiée de compte utilisateur et d’offrir à moindre frais une plateforme de gestion de fichiers simplifiée et dynamique à un secteur manquant de moyens financiers ou de recul sur les possibilités technologiques offertes.

## Périmètre fonctionnel

Cette application doit permettre de :

..* Créer des comptes utilisateurs
..* Créer des études
..* Créer des étapes liées aux études
..* Gérer un QC simple (conforme/non conforme)
..* Donner des droits spécifiques aux utilisateurs vis-à-vis des études
..* Gérer les utilisateurs en les liants à des centres
..* Permettre de charger les documents selon un rangement centre / étude / patient 
..* Permettre d’affilier des étapes aux fichiers 
..* Permettre d’afficher les statiques liées aux données récupérées

L’application doit recenser :

..* Les études, les étapes, les centres
..* Les statistiques pour les administrateurs de la plateforme
..* Un système d’authentification pour les administrateurs et les utilisateurs

## Périmètre technique

..* Python 3.6
..* Django 3.0.8
..* postgreSQL 12.3

## Chargement des données des tables de référence

Utiliser la commande personnel django :

... `python manage.py loaddataref`

## Chargement des données tests

Utiliser la commande personnel django :

... `python manage.py loaddatatest`

## Paramétrage du chemin de chargement

L'application permet de charger des documents et d'arranger le chemin de sauvegarde pour classer les fichiers tous le temps de la même manière.
Ce chemin peut être modifié via le module *"user_directory_path"* que vous trouverez dans l'application *"upload"* et dans le __fichier models__.
Les paramètres de base enregistre les données dans : __DATA/NOM_ETUDE/NOM_CENTRE/ID_PATIENT/NOM_FICHIER__

Référez-vous au module *"doc_directory_path"* pour modifier les chemins de sauvegarde des documents. 
Les paramètres de base enregistre les documents dans : __DATA/documents/NOM_DOCUMENT__

## Paramétrage du super utilisateur

Utiliser la commande django :

... `python manage.py createsuperuser`

## Gestion des groupes

Il éxiste deux groupes : Utilisateur ou Administrateur
..* Utilisateur : Peuvent voir l'index, la partie chargement de document et la partie contact
..* Administrateur : Possède les mêmes droits que le groupe utilisateur, mais on accès aussi à la partie administrateur 

## Créer votre premier utilisateur

En vous connectant avec votre compte super utilisateur, vous avez accès à la partie __"Administration"__ .
Dans le menu à gauche vous trouvez une section __"Ajouter un utilisateur"__ 
Dans cette partie vous pouvez indiquer si c'est un utilisateur standard ou un administrateur.

## Envois de fichier

L'envois de fichier est géré par le formulaire d'upload qui se trouve dans la partie __"Formulaire d'upload"__ .
Les points à renseigner sont :

..* Numero de patient : Déterminer par les équipes et l'étude
..* Etude : Liée à l'utilisateur connecté
..* Date examen : Entrée par l'utilisateur
..* Upload : Permet de charger les documents

## Paramétrage

L'application est paramétrable pour permettre un meilleur suivi, cela se retrouve dans la partie "Administration" :

..* __"Ajouter des études"__ : Cette partie permet d'ajouter des études à la base de donnée
..* __"Création des étapes"__ : Permet de lier des étapes aux études
..* __"Ajouter un centre"__ : Permet de créer des centres composé d'un nom et d'un numéro
..* __"Ajouter un utilisateur"__ : Permet de créer de nouveau utilisateur de l'application
..* __"Gestion documentaire"__ : Permet de partager des notes avec certain utilisateur selon l'études
..* __"Autorisation des utilisateurs"__ : Permet d'octroyer un centre et des études à un utilisateur
..* __"Gestion documentaire"__ : Permet de partager des documents avec les autres utilisateurs

## Gestion documentaire

L'application possède une partie de gestion documentaire.
Il est possible de créer des notes avec un document attaché, ces notes sont liée à des études et ne seront disponible unquement aux utilisateurs possédant le droit sur cette études. 

