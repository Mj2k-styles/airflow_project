#!/bin/bash
# Script de lancement rapide d'Airflow dans WSL
# Usage: ./start_airflow.sh

set -e

echo "=========================================="
echo "   Démarrage d'Airflow"
echo "=========================================="
echo ""

cd /mnt/c/Users/jmike/OneDrive/Desktop/airflow_project-1

echo "1. Activation de l'environnement virtuel..."
source venv/bin/activate

echo "2. Configuration de AIRFLOW_HOME..."
export AIRFLOW_HOME=/mnt/c/Users/jmike/OneDrive/Desktop/airflow_project-1

echo "3. Initialisation de la base de données (si nécessaire)..."
if [ ! -f "airflow.db" ]; then
    echo "   Création de la base de données Airflow..."
    airflow db migrate
    
    echo "   Création de l'utilisateur admin..."
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com \
        --password admin
else
    echo "   ✓ Base de données déjà initialisée"
fi

echo ""
echo "4. Vérification des DAGs..."
airflow dags list 2>&1 | grep -i "openweather" && echo "   ✓ DAG trouvé !" || echo "   ⚠️ DAG non trouvé"

echo ""
echo "=========================================="
echo "5. Lancement d'Airflow Standalone..."
echo "=========================================="
echo ""
echo "Interface web: http://localhost:8080"
echo "Login: admin"
echo "Password: admin"
echo ""

airflow standalone
