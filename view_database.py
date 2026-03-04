"""
Script utilitaire pour consulter les données météo dans la base SQLite
Usage: python view_database.py
"""

import sqlite3
import pandas as pd
from datetime import datetime

def view_weather_data(db_path="/tmp/weather_data.db"):
    """
    Affiche les données météo stockées dans la base SQLite
    """
    try:
       
        conn = sqlite3.connect(db_path)
        
        print("=" * 80)
        print("🌤️  BASE DE DONNÉES MÉTÉO - VISUALISATION")
        print("=" * 80)
        print(f"\n📍 Base de données: {db_path}\n")
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM weather_data")
        total_records = cursor.fetchone()[0]
        print(f"📊 Nombre total d'enregistrements: {total_records}\n")
        
        if total_records == 0:
            print("⚠️  Aucune donnée trouvée dans la base de données.")
            print("   Exécutez d'abord le DAG Airflow pour insérer des données.\n")
            conn.close()
            return
        
        # Récupérer toutes les données
        query = "SELECT * FROM weather_data ORDER BY id DESC"
        df = pd.read_csv(db_path, sep=',') if False else pd.read_sql_query(query, conn)
        
        # Afficher les statistiques
        print("📈 STATISTIQUES DES DONNÉES")
        print("-" * 80)
        
        if 'temperature_celsius' in df.columns:
            print(f"🌡️  Température moyenne: {df['temperature_celsius'].mean():.2f}°C")
            print(f"🌡️  Température min: {df['temperature_celsius'].min():.2f}°C")
            print(f"🌡️  Température max: {df['temperature_celsius'].max():.2f}°C")
        
        if 'humidity' in df.columns:
            print(f"💧 Humidité moyenne: {df['humidity'].mean():.2f}%")
        
        if 'wind_speed_kmh' in df.columns:
            print(f"💨 Vitesse du vent moyenne: {df['wind_speed_kmh'].mean():.2f} km/h")
        
        print("\n" + "=" * 80)
        print("📋 DERNIERS ENREGISTREMENTS (5 plus récents)")
        print("=" * 80 + "\n")
        
        # Sélectionner les colonnes importantes à afficher
        columns_to_display = [
            'id', 'city', 'temperature_celsius', 'feels_like_celsius',
            'humidity', 'weather_description', 'date_time'
        ]
        
        # Vérifier quelles colonnes existent
        available_columns = [col for col in columns_to_display if col in df.columns]
        
        # Afficher les 5 derniers enregistrements
        print(df[available_columns].head(5).to_string(index=False))
        
        print("\n" + "=" * 80)
        print("🔍 DÉTAILS DU DERNIER ENREGISTREMENT")
        print("=" * 80 + "\n")
        
        # Afficher toutes les colonnes du dernier enregistrement
        last_record = df.iloc[0]
        for col in df.columns:
            if col != 'id':
                print(f"  {col:.<30} {last_record[col]}")
        
        print("\n" + "=" * 80)
        print("✅ Consultation terminée avec succès!")
        print("=" * 80 + "\n")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Erreur de base de données: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def export_to_csv(db_path="/tmp/weather_data.db", output_file="weather_data_export.csv"):
    """
    Exporte les données de la base SQLite vers un fichier CSV
    """
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM weather_data", conn)
        df.to_csv(output_file, index=False)
        print(f"✅ Données exportées vers: {output_file}")
        print(f"📊 Nombre d'enregistrements exportés: {len(df)}")
        conn.close()
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")

if __name__ == "__main__":
    import sys
    
    # Vérifier les arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "export":
            output_file = sys.argv[2] if len(sys.argv) > 2 else "weather_data_export.csv"
            export_to_csv(output_file=output_file)
        else:
            print("Usage:")
            print("  python view_database.py           # Afficher les données")
            print("  python view_database.py export    # Exporter vers CSV")
    else:
        view_weather_data()
