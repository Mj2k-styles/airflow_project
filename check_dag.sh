#!/bin/bash
# Script de diagnostic pour vérifier pourquoi le DAG n'apparaît pas

echo "=========================================="
echo "DIAGNOSTIC AIRFLOW DAG"
echo "=========================================="
echo ""

cd /mnt/c/Users/jmike/OneDrive/Desktop/airflow_project-1
source venv/bin/activate

export AIRFLOW_HOME=/mnt/c/Users/jmike/OneDrive/Desktop/airflow_project-1

echo "1. Vérification de AIRFLOW_HOME:"
echo "   AIRFLOW_HOME = $AIRFLOW_HOME"
echo ""

echo "2. Vérification du fichier de configuration:"
if [ -f "airflow.cfg" ]; then
    echo "   ✓ airflow.cfg existe"
    DAGS_FOLDER=$(grep "^dags_folder" airflow.cfg | cut -d'=' -f2 | xargs)
    echo "   dags_folder = $DAGS_FOLDER"
else
    echo "   ⚠️ airflow.cfg n'existe pas - exécutez: airflow db init"
fi
echo ""

echo "3. DAGs disponibles:"
airflow dags list 2>&1 | grep -v "INFO\|WARNING" | head -20
echo ""

echo "4. Erreurs du DAG openweather_etl_pipeline:"
airflow dags list-import-errors 2>&1 | grep -A 5 "openweather" || echo "   Aucune erreur trouvée"
echo ""

echo "5. Test d'importation Python du DAG:"
python -c "import sys; sys.path.insert(0, 'dags'); import etl; print('✓ DAG importé avec succès')" 2>&1
echo ""

echo "=========================================="
echo "Pour relancer Airflow:"
echo "  export AIRFLOW_HOME=/mnt/c/Users/jmike/OneDrive/Desktop/airflow_project-1"
echo "  source venv/bin/activate"
echo "  airflow standalone"
echo "=========================================="
