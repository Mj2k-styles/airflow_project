"""
Pipeline ETL avec Apache Airflow et OpenWeatherMap API
Auteur: Data Engineering Project
Date: Mars 2026
"""

from airflow import DAG
from airflow.sdk import task
from datetime import datetime, timedelta
import logging
import pandas as pd
import sqlite3
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="openweather_etl_pipeline",
    default_args=default_args,
    schedule='*/5 * * * *',
    start_date=datetime(2026, 3, 1),
    description="Pipeline ETL pour extraire les données météo depuis OpenWeatherMap API",
    catchup=False,
) as dag:

    @task
    def extract_weather_data():
        """
        Extraction des données météo depuis l'API OpenWeatherMap.
        Extrait au minimum 7 variables météorologiques.
        """
        try:
            # Récupérer la clé API depuis les variables d'environnement
            api_key = os.getenv('OPENWEATHER_API_KEY')
            city = os.getenv('WEATHER_CITY', 'Paris')
            
            if not api_key:
                logging.error("OPENWEATHER_API_KEY n'est pas défini dans les variables d'environnement!")
                raise ValueError("API key manquante")
            
            # URL de l'API OpenWeatherMap
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            
            logging.info(f"Extraction des données météo pour la ville: {city}")
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Extraire minimum 7 variables
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],  # En Kelvin
                'feels_like': data['main']['feels_like'],  # En Kelvin
                'humidity': data['main']['humidity'],  # En pourcentage
                'pressure': data['main']['pressure'],  # En hPa
                'wind_speed': data['wind']['speed'],  # En m/s
                'weather_description': data['weather'][0]['description'],
                'timestamp': data['dt'],  # Unix timestamp
                'visibility': data.get('visibility', 0),  # En mètres
            }
            
            # Créer un DataFrame
            df = pd.DataFrame([weather_data])
            
            # Sauvegarder les données brutes
            file_path = '/tmp/raw_weather_data.csv'
            df.to_csv(file_path, index=False)
            
            logging.info(f"✅ Données extraites avec succès: {len(df)} enregistrement(s)")
            logging.info(f"Variables extraites: {list(weather_data.keys())}")
            logging.info(f"Données sauvegardées dans: {file_path}")
            
            return file_path
            
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Erreur lors de la requête API: {e}")
            raise
        except Exception as e:
            logging.error(f"❌ Erreur lors de l'extraction des données: {e}")
            raise

    @task
    def transform_weather_data(file_path):
        """
        Transformation des données météo.
        Effectue au minimum 5 transformations sur les données.
        """
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Chargement des données depuis: {file_path}")
            logging.info(f"Nombre d'enregistrements avant transformation: {len(df)}")
            
            # TRANSFORMATION 1: Convertir la température de Kelvin en Celsius
            df['temperature_celsius'] = df['temperature'] - 273.15
            df['temperature_celsius'] = df['temperature_celsius'].round(2)
            logging.info("✅ Transformation 1: Température convertie en Celsius")
            
            # TRANSFORMATION 2: Convertir la température ressentie de Kelvin en Celsius
            df['feels_like_celsius'] = df['feels_like'] - 273.15
            df['feels_like_celsius'] = df['feels_like_celsius'].round(2)
            logging.info("✅ Transformation 2: Température ressentie convertie en Celsius")
            
            # TRANSFORMATION 3: Convertir le timestamp Unix en datetime lisible
            df['date_time'] = pd.to_datetime(df['timestamp'], unit='s')
            df['date_time'] = df['date_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            logging.info("✅ Transformation 3: Timestamp converti en datetime")
            
            # TRANSFORMATION 4: Créer une catégorie de température
            def categorize_temperature(temp):
                if temp < 10:
                    return 'Froid'
                elif temp < 20:
                    return 'Modéré'
                elif temp < 30:
                    return 'Chaud'
                else:
                    return 'Très Chaud'
            
            df['temperature_category'] = df['temperature_celsius'].apply(categorize_temperature)
            logging.info("✅ Transformation 4: Catégorie de température créée")
            
            # TRANSFORMATION 5: Calculer un index de confort (basé sur température et humidité)
            # Index de confort = température - (humidité / 5)
            df['comfort_index'] = (df['temperature_celsius'] - (df['humidity'] / 5)).round(2)
            logging.info("✅ Transformation 5: Index de confort calculé")
            
            # TRANSFORMATION 6 (bonus): Formater la description météo en majuscules
            df['weather_description'] = df['weather_description'].str.upper()
            logging.info("✅ Transformation 6 (bonus): Description formatée en majuscules")
            
            # TRANSFORMATION 7 (bonus): Convertir la vitesse du vent en km/h
            df['wind_speed_kmh'] = (df['wind_speed'] * 3.6).round(2)
            logging.info("✅ Transformation 7 (bonus): Vitesse du vent convertie en km/h")
            
            # Sauvegarder les données transformées
            transformed_file_path = '/tmp/transformed_weather_data.csv'
            df.to_csv(transformed_file_path, index=False)
            
            logging.info(f"✅ Transformations terminées avec succès")
            logging.info(f"Nombre de colonnes après transformation: {len(df.columns)}")
            logging.info(f"Données transformées sauvegardées dans: {transformed_file_path}")
            
            return transformed_file_path
            
        except Exception as e:
            logging.error(f"❌ Erreur lors de la transformation des données: {e}")
            raise

    @task
    def load_to_database(transformed_file_path):
        """
        Chargement des données transformées dans une base de données SQLite.
        """
        # Utiliser le dossier du projet (AIRFLOW_HOME)
        db_path = os.path.join(os.getenv('AIRFLOW_HOME', '.'), 'weather_data.db')
        try:
            df = pd.read_csv(transformed_file_path)
            logging.info(f"Chargement des données depuis: {transformed_file_path}")
            logging.info(f"Nombre d'enregistrements à charger: {len(df)}")
            
            # Connexion à la base de données SQLite
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Créer la table si elle n'existe pas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT NOT NULL,
                    country TEXT,
                    temperature REAL,
                    feels_like REAL,
                    temperature_celsius REAL,
                    feels_like_celsius REAL,
                    humidity INTEGER,
                    pressure INTEGER,
                    wind_speed REAL,
                    wind_speed_kmh REAL,
                    weather_description TEXT,
                    visibility INTEGER,
                    timestamp INTEGER,
                    date_time TEXT,
                    temperature_category TEXT,
                    comfort_index REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logging.info("✅ Table 'weather_data' créée ou déjà existante")
            
            # Charger les données dans la table
            df.to_sql("weather_data", conn, if_exists='append', index=False)
            
            # Vérifier le nombre d'enregistrements
            cursor.execute("SELECT COUNT(*) FROM weather_data")
            count = cursor.fetchone()[0]
            
            logging.info(f"✅ Données chargées avec succès dans la base de données")
            logging.info(f"Base de données: {db_path}")
            logging.info(f"Nombre total d'enregistrements dans la table: {count}")
            
            # Afficher un aperçu des dernières données chargées
            cursor.execute("SELECT * FROM weather_data ORDER BY id DESC LIMIT 1")
            last_record = cursor.fetchone()
            logging.info(f"Dernier enregistrement: {last_record}")
            
            conn.close()
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Erreur lors du chargement des données: {e}")
            raise

    @task
    def verify_data():
        """
        Vérification des données chargées dans la base de données.
        """
        try:
            db_path = os.path.join(os.getenv('AIRFLOW_HOME', '.'), 'weather_data.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Compter le nombre total d'enregistrements
            cursor.execute("SELECT COUNT(*) FROM weather_data")
            total_count = cursor.fetchone()[0]
            
            # Récupérer les derniers enregistrements
            cursor.execute("SELECT * FROM weather_data ORDER BY id DESC LIMIT 5")
            records = cursor.fetchall()
            
            logging.info("=" * 60)
            logging.info("📊 VÉRIFICATION DES DONNÉES")
            logging.info("=" * 60)
            logging.info(f"Nombre total d'enregistrements: {total_count}")
            logging.info(f"\nDerniers enregistrements:")
            
            for record in records:
                logging.info(f"  - ID: {record[0]} | Ville: {record[1]} | Temp: {record[5]}°C | {record[11]}")
            
            logging.info("=" * 60)
            
            conn.close()
            
            return f"✅ Vérification terminée: {total_count} enregistrement(s) dans la base"
            
        except Exception as e:
            logging.error(f"❌ Erreur lors de la vérification: {e}")
            raise

    @task
    def export_to_csv():
        """
        Export des données de la base SQLite vers un fichier CSV.
        """
        try:
            db_path = os.path.join(os.getenv('AIRFLOW_HOME', '.'), 'weather_data.db')
            csv_path = os.path.join(os.getenv('AIRFLOW_HOME', '.'), 'weather_export.csv')
            
            logging.info(f"Export des données depuis: {db_path}")
            
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT * FROM weather_data", conn)
            conn.close()
            
            # Exporter vers CSV
            df.to_csv(csv_path, index=False)
            
            logging.info(f"✅ Export réussi: {len(df)} lignes exportées")
            logging.info(f"Fichier CSV: {csv_path}")
            
            return csv_path
            
        except Exception as e:
            logging.error(f"❌ Erreur lors de l'export CSV: {e}")
            raise

    # Définir le workflow
    raw_data_path = extract_weather_data()
    transformed_data_path = transform_weather_data(raw_data_path)
    load_result = load_to_database(transformed_data_path)
    verify_result = verify_data()
    csv_export = export_to_csv()
    
    # Définir les dépendances
    load_result >> verify_result >> csv_export