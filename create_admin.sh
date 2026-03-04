#!/bin/bash
# Script pour créer l'utilisateur admin Airflow
# Usage: ./create_admin.sh

cd /mnt/c/Users/jmike/OneDrive/Desktop/airflow_project-1
source venv/bin/activate
export AIRFLOW_HOME=/mnt/c/Users/jmike/OneDrive/Desktop/airflow_project-1

echo "Création de l'utilisateur admin..."
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

echo ""
echo "✓ Utilisateur créé avec succès !"
echo ""
echo "Identifiants de connexion:"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "Accédez à: http://localhost:8080"
