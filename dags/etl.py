from airflow import DAG
from airflow.sdk import task
from datetime import datetime, timedelta
import logging
from faker import Faker
import pandas as pd
import sqlite3

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="workflow_etl",
    default_args=default_args,
    schedule='@daily',
    start_date=datetime(2026, 2, 24),
    description="Premier pipeline ETL pour Airflow",
) as dag:

    @task
    def ingest_data():
        try:
            fake = Faker()
            data = []
            for i in range(10):
                data.append({
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "country": fake.country(),
                    "dob": fake.date_of_birth(),
                })
            df = pd.DataFrame(data)
            file_path = '/tmp/fake_data.csv'
            df.to_csv(file_path, index=False)
            logging.info(f"Data ingested and saved to {file_path}")
        except Exception as e:
            logging.error(f"Error ingesting data: {e}")
            return None
        return file_path

    @task
    def transform_data(file_path):
        try:
            df = pd.read_csv(file_path)
            df['full_name'] = df['first_name'] + ' ' + df['last_name']
            transformed_file_path = '/tmp/transformed_data.csv'
            df.to_csv(transformed_file_path, index=False)
            logging.info(f"Data transformed and saved to {transformed_file_path}")
        except Exception as e:
            logging.error(f"Error transforming data: {e}")
            return None
        return transformed_file_path

    @task
    def load_data(transformed_file_path, db_path="/tmp/users.db"):
        try:
            df = pd.read_csv(transformed_file_path)
            logging.info(f"Data loaded from {transformed_file_path}")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    country TEXT,
                    dob TEXT,
                    full_name TEXT
                )
            ''')
            conn.commit()
            df.to_sql("users", conn, if_exists='append', index=False)
            logging.info(f"Data loaded into database {db_path}")
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            return False

    file_path = ingest_data()
    transformed_file_path = transform_data(file_path)
    load_data(transformed_file_path)