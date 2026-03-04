@echo off
REM ================================================
REM Script de configuration et démarrage d'Airflow
REM Pour Windows
REM ================================================

echo.
echo ========================================
echo   Configuration du Projet Airflow
echo ========================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\" (
    echo [1/6] Creation de l'environnement virtuel...
    python -m venv venv
    echo ✓ Environnement virtuel cree
) else (
    echo [1/6] Environnement virtuel deja present
)

echo.
echo [2/6] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo [3/6] Installation des dependances...
pip install -r requirements.txt --quiet

echo.
echo [4/6] Configuration d'Airflow...
set AIRFLOW_HOME=%CD%

REM Vérifier si Airflow est déjà initialisé
if not exist "airflow.db" (
    echo Initialisation de la base de donnees Airflow...
    airflow db migrate
    
    echo.
    echo Creation de l'utilisateur admin...
    airflow users create ^
        --username admin ^
        --firstname Admin ^
        --lastname User ^
        --role Admin ^
        --email admin@example.com ^
        --password admin
    
    echo ✓ Airflow initialise avec succes
) else (
    echo ✓ Airflow deja initialise
)

echo.
echo [5/6] Verification du fichier .env...
if not exist ".env" (
    echo ⚠️  ATTENTION: Le fichier .env n'existe pas!
    echo    Copiez .env.example vers .env et ajoutez votre cle API
    echo    Commande: copy .env.example .env
    pause
) else (
    echo ✓ Fichier .env present
)

echo.
echo ========================================
echo   Configuration terminee!
echo ========================================
echo.
echo 📝 Prochaines etapes:
echo    1. Editez le fichier .env avec votre cle API OpenWeatherMap
echo    2. Lancez Airflow avec: airflow standalone
echo    3. Ouvrez http://localhost:8080 dans votre navigateur
echo    4. Connectez-vous avec: admin / admin
echo.
echo Pour demarrer Airflow maintenant, tapez: airflow standalone
echo.

pause
