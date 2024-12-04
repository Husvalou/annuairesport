# Annuaire Sport Tarn

Application web permettant de répertorier et rechercher les clubs sportifs du Tarn.

## Fonctionnalités

- Création et gestion de fiches de clubs sportifs
- Recherche multicritères (sport, ville, âge, etc.)
- Système d'authentification
- Gestion des photos
- Interface d'administration

## Prérequis

- Python 3.8 ou supérieur
- Navigateur web moderne
- Connexion Internet (pour les CDN Bootstrap)

## Installation

1. Clonez ou téléchargez ce dépôt
2. Double-cliquez sur `install.bat` pour installer l'application
   - Crée l'environnement virtuel
   - Installe les dépendances
   - Initialise la base de données
   - Crée les dossiers nécessaires

## Lancement de l'application

1. Ouvrez une invite de commande dans le dossier du projet
2. Activez l'environnement virtuel :
   ```
   venv\Scripts\activate
   ```
3. Lancez le serveur :
   ```
   python app.py
   ```
4. Ouvrez votre navigateur à l'adresse : http://localhost:5000

## Compte administrateur par défaut

- Email : admin@annuairesport.fr
- Mot de passe : admin123

**Important** : Changez ces identifiants en production !

## Structure du projet

- `app.py` : Application principale Flask
- `models.py` : Modèles de données
- `forms.py` : Formulaires WTForms
- `templates/` : Templates HTML
- `static/` : Fichiers statiques (CSS, JS, images)
- `static/uploads/` : Photos des clubs uploadées

## Développement

Pour contribuer au projet :

1. Créez une branche pour votre fonctionnalité
2. Développez et testez votre code
3. Soumettez une pull request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
