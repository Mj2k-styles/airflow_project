# 🌤️ Pipeline ETL - OpenWeatherMap avec Apache Airflow

## 📋 Description du Projet

Ce projet implémente une pipeline de données ETL (Extract, Transform, Load) complète utilisant Apache Airflow pour orchestrer le workflow. La pipeline extrait des données météorologiques depuis l'API OpenWeatherMap, effectue plusieurs transformations, et charge les données dans une base de données SQLite.

**Auteur:** TP2 Data Engineering  
**Date:** Mars 2026

---

## 🎯 Objectifs du Projet

✅ Extraire des données depuis l'API OpenWeatherMap (minimum 7 variables)  
✅ Effectuer au minimum 5 transformations sur les données  
✅ Charger les données transformées dans une base SQLite  
✅ Orchestrer le workflow avec Apache Airflow  
✅ Utiliser les variables d'environnement pour sécuriser la clé API

---

## 📊 Variables Extraites (10 au total)

1. **city** - Nom de la ville
2. **country** - Code du pays
3. **temperature** - Température en Kelvin
4. **feels_like** - Température ressentie en Kelvin
5. **humidity** - Taux d'humidité (%)
6. **pressure** - Pression atmosphérique (hPa)
7. **wind_speed** - Vitesse du vent (m/s)
8. **weather_description** - Description de la météo
9. **timestamp** - Horodatage Unix
10. **visibility** - Visibilité (mètres)

---

## 🔄 Transformations Effectuées (7 au total)

1. **Conversion température Kelvin → Celsius**
2. **Conversion température ressentie Kelvin → Celsius**
3. **Conversion timestamp Unix → DateTime lisible**
4. **Création de catégories de température** (Froid, Modéré, Chaud, Très Chaud)
5. **Calcul d'un index de confort** (température - humidité/5)
6. **Formatage de la description** (en majuscules)
7. **Conversion vitesse du vent** (m/s → km/h)

---

## 🛠️ Installation et Configuration

### Prérequis

- Python 3.11 ou supérieur
- pip / uv (gestionnaire de paquets Python)

### Étape 1 : Créer un environnement virtuel

#### Avec venv :

```bash
python -m venv venv
# Sur Windows
venv\Scripts\activate
# Sur Linux/Mac
source venv/bin/activate
```

#### Avec uv (recommandé) :

```bash
uv venv
# Sur Windows
.venv\Scripts\activate
# Sur Linux/Mac
source .venv/bin/activate
```

### Étape 2 : Installer les dépendances

#### Avec pip :

```bash
pip install -r requirements.txt
```

#### Avec uv (plus rapide) :

```bash
uv pip install -r requirements.txt
```

### Étape 3 : Obtenir une clé API OpenWeatherMap

1. Allez sur [OpenWeatherMap](https://openweathermap.org/api)
2. Créez un compte gratuit
3. Générez votre clé API
4. Copiez la clé API

### Étape 4 : Configurer les variables d'environnement

1. Copiez le fichier `.env.example` en `.env` :

```bash
copy .env.example .env    # Windows
# ou
cp .env.example .env      # Linux/Mac
```

2. Éditez le fichier `.env` et ajoutez votre clé API :

```env
OPENWEATHER_API_KEY=votre_vraie_cle_api_ici
WEATHER_CITY=Paris
```

### Étape 5 : Initialiser Airflow

```bash
# Définir le répertoire Airflow
set AIRFLOW_HOME=%CD%    # Windows
# ou
export AIRFLOW_HOME=$(pwd)    # Linux/Mac

# Initialiser la base de données Airflow
airflow db init

# Créer un utilisateur admin
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

### Étape 6 : Démarrer Airflow

#### Option 1 : Mode standalone (recommandé pour développement)

```bash
airflow standalone
```

#### Option 2 : Démarrer séparément le scheduler et le webserver

Terminal 1 :

```bash
airflow scheduler
```

Terminal 2 :

```bash
airflow webserver --port 8080
```

### Étape 7 : Accéder à l'interface Airflow

Ouvrez votre navigateur et allez sur : [http://localhost:8080](http://localhost:8080)

- **Utilisateur :** admin
- **Mot de passe :** admin

---

## 🚀 Utilisation

### 1. Activer le DAG

Dans l'interface Airflow :

1. Cherchez le DAG `openweather_etl_pipeline`
2. Cliquez sur le bouton toggle pour l'activer
3. Le DAG s'exécutera automatiquement selon le planning (quotidien)

### 2. Exécuter manuellement le DAG

Cliquez sur le bouton "▶️ Trigger DAG" pour lancer immédiatement une exécution.

### 3. Consulter les logs

1. Cliquez sur le DAG
2. Cliquez sur l'exécution (DAG run)
3. Cliquez sur une tâche (task)
4. Cliquez sur "Logs" pour voir les détails

---

## 📁 Structure du Projet

```
airflow_project-1/
│
├── dags/
│   └── etl.py                    # DAG principal avec le pipeline ETL
│
├── .env                          # Variables d'environnement (à créer)
├── .env.example                  # Exemple de configuration
├── .gitignore                    # Fichiers à ignorer par Git
├── pyproject.toml                # Configuration du projet et dépendances
├── requirements.txt              # Dépendances Python
├── README.md                     # Documentation (ce fichier)
└── main.py                       # Script principal (optionnel)
```

---

## 🗄️ Base de Données SQLite

Les données sont stockées dans `/tmp/weather_data.db` avec la structure suivante :

### Table : `weather_data`

| Colonne              | Type      | Description                      |
| -------------------- | --------- | -------------------------------- |
| id                   | INTEGER   | Clé primaire auto-incrémentée    |
| city                 | TEXT      | Nom de la ville                  |
| country              | TEXT      | Code du pays                     |
| temperature          | REAL      | Température en Kelvin            |
| feels_like           | REAL      | Température ressentie en Kelvin  |
| temperature_celsius  | REAL      | Température en Celsius           |
| feels_like_celsius   | REAL      | Température ressentie en Celsius |
| humidity             | INTEGER   | Humidité (%)                     |
| pressure             | INTEGER   | Pression (hPa)                   |
| wind_speed           | REAL      | Vitesse du vent (m/s)            |
| wind_speed_kmh       | REAL      | Vitesse du vent (km/h)           |
| weather_description  | TEXT      | Description météo                |
| visibility           | INTEGER   | Visibilité (m)                   |
| timestamp            | INTEGER   | Timestamp Unix                   |
| date_time            | TEXT      | Date et heure lisible            |
| temperature_category | TEXT      | Catégorie de température         |
| comfort_index        | REAL      | Index de confort                 |
| created_at           | TIMESTAMP | Date de création                 |

### Consulter les données

```bash
# Sur Windows WSL ou Linux/Mac
sqlite3 /tmp/weather_data.db

# Dans SQLite
SELECT * FROM weather_data ORDER BY id DESC LIMIT 10;
.exit
```

---

## 📸 Livrables

Pour valider le TP, fournissez :

1. ✅ **Projet compressé** (Nom_Prenom.zip)
2. ✅ **Screenshot de l'UI Airflow** montrant les tâches du DAG
3. ✅ **Screenshots des Logs** de chaque tâche (Extract, Transform, Load, Verify)
4. ✅ **Screenshot de la base de données** SQLite avec les données chargées

---

## 🔧 Dépannage

### Problème : "OPENWEATHER_API_KEY n'est pas défini"

**Solution :** Vérifiez que le fichier `.env` existe et contient votre clé API.

### Problème : "Module 'dotenv' introuvable"

**Solution :** Installez la dépendance :

```bash
pip install python-dotenv
```

### Problème : erreur 401 de l'API

**Solution :** Votre clé API est invalide ou a expiré. Générez-en une nouvelle.

### Problème : Airflow ne trouve pas le DAG

**Solution :** Vérifiez que `AIRFLOW_HOME` pointe vers le bon répertoire et que le dossier `dags/` existe.

---

## 📚 Ressources

- [Documentation Apache Airflow](https://airflow.apache.org/docs/)
- [API OpenWeatherMap](https://openweathermap.org/api)
- [Documentation Python dotenv](https://pypi.org/project/python-dotenv/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## ✨ Améliorations Possibles

- Ajouter plusieurs villes dans la configuration
- Implémenter des alertes par email
- Créer des visualisations avec Matplotlib/Plotly
- Ajouter un export vers CSV ou Excel
- Implémenter un système de cache
- Ajouter des tests unitaires

---

## 📝 Licence

Projet académique - TP2 Data Engineering - Mars 2026

---

## 👤 Contact

Pour toute question sur ce projet, contactez votre enseignant ou référez-vous à la documentation officielle d'Airflow.
