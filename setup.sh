#!/bin/bash
# ================================================
# Script de configuration et démarrage d'Airflow
# Pour Linux/Mac
# ================================================

echo ""
echo "========================================"
echo "   Configuration du Projet Airflow"
echo "========================================"
echo ""

# Vérifier si l'environnement virtuel Linux est valide
if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
    echo "[1/6] Création de l'environnement virtuel Linux..."
    rm -rf venv
    python3 -m venv venv
    echo "✓ Environnement virtuel créé"
else
    echo "[1/6] Environnement virtuel déjà présent"
fi

echo ""
echo "[2/6] Activation de l'environnement virtuel..."
source venv/bin/activate

echo ""
echo "[3/6] Installation des dépendances..."
pip install -r requirements.txt --quiet

if ! command -v airflow >/dev/null 2>&1; then
    echo "❌ Airflow n'a pas été trouvé après l'installation."
    echo "   Essayez: pip install apache-airflow"
    exit 1
fi

echo ""
echo "[4/6] Configuration d'Airflow..."
export AIRFLOW_HOME=$(pwd)


if [ ! -f "airflow.db" ]; then
    echo "Initialisation de la base de données Airflow..."
    airflow db migrate
    
    echo ""
    echo "Création de l'utilisateur admin..."
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com \
        --password admin
    
    echo "✓ Airflow initialisé avec succès"
else
    echo "✓ Airflow déjà initialisé"
fi

echo ""
echo "[5/6] Vérification du fichier .env..."
if [ ! -f ".env" ]; then
    echo "⚠️  ATTENTION: Le fichier .env n'existe pas!"
    echo "   Copiez .env.example vers .env et ajoutez votre clé API"
    echo "   Commande: cp .env.example .env"
    read -p "Appuyez sur Entrée pour continuer..."
else
    echo "✓ Fichier .env présent"
fi

echo ""
echo "========================================"
echo "   Configuration terminée!"
echo "========================================"
echo ""
echo "📝 Prochaines étapes:"
echo "   1. Éditez le fichier .env avec votre clé API OpenWeatherMap"
echo "   2. Lancez Airflow avec: airflow standalone"
echo "   3. Ouvrez http://localhost:8080 dans votre navigateur"
echo "   4. Connectez-vous avec: admin / admin"
echo ""
echo "Pour démarrer Airflow maintenant, tapez: airflow standalone"
echo ""
