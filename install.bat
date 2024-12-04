@echo off
echo Installation de l'Annuaire Sport Tarn
echo ===================================

:: Vérifier si Python est installé
python --version > nul 2>&1
if errorlevel 1 (
    echo Python n'est pas installé. Veuillez installer Python 3.8 ou supérieur.
    exit /b 1
)

:: Créer l'environnement virtuel
echo Creation de l'environnement virtuel...
python -m venv venv

:: Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate

:: Installer les dépendances
echo Installation des dependances...
pip install -r requirements.txt

:: Créer les dossiers nécessaires
echo Creation des dossiers...
mkdir static 2>nul
mkdir static\uploads 2>nul

:: Initialiser la base de données
echo Initialisation de la base de donnees...
python -c "from models import init_db; init_db()"

echo Installation terminee avec succes !
echo Pour lancer l'application :
echo 1. Activez l'environnement virtuel : venv\Scripts\activate
echo 2. Lancez le serveur : python app.py
pause
