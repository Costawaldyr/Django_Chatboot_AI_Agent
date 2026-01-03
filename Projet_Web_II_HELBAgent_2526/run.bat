@echo off
echo ======================================
echo  Lancement du projet Django HELBAgent
echo ======================================

if not exist ".venv" (
    python -m venv .venv
)

call .venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

echo  Démarrage du serveur Django...
cd HELBAgent
python manage.py makemigrations
python manage.py migrate

start http://127.0.0.1:8000/

python manage.py runserver

pause
