# 🚀 GUIDE DE DÉMARRAGE RAPIDE

## Installation Express (5 minutes)

### 1️⃣ Cloner et naviguer

```bash
cd airflow_project-1
```

### 2️⃣ Configurer automatiquement (Windows)

```bash
setup.bat
```

### 2️⃣ Configurer automatiquement (Linux/Mac)

```bash
chmod +x setup.sh
./setup.sh
```

### 3️⃣ Configurer la clé API

```bash
# Copier le template
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# Éditer .env et ajouter votre clé API OpenWeatherMap
# OPENWEATHER_API_KEY=votre_cle_ici
```

### 4️⃣ Démarrer Airflow

```bash
# Activer l'environnement virtuel si nécessaire
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/Mac

# Lancer Airflow
airflow standalone
```

### 5️⃣ Accéder à l'interface

- URL: http://localhost:8080
- Login: `admin`
- Password: `admin`

### 6️⃣ Activer et exécuter le DAG

1. Trouvez `openweather_etl_pipeline` dans la liste
2. Activez-le avec le toggle
3. Cliquez sur "▶️ Trigger DAG"

### 7️⃣ Consulter les résultats

```bash
# Voir les données dans la base
python view_database.py

# Exporter en CSV
python view_database.py export
```

---

## 📸 Screenshots Requis pour le TP

1. **UI Airflow**: Vue du DAG avec toutes les tâches
2. **Logs Extract**: Logs de la tâche d'extraction
3. **Logs Transform**: Logs des transformations
4. **Logs Load**: Logs du chargement SQLite
5. **Base de données**: Contenu de la table weather_data

---

## 🆘 Aide Rapide

### Problème: Module introuvable

```bash
pip install -r requirements.txt
```

### Problème: "airflow db init" n'existe plus

Utilisez la commande Airflow 3.x :

```bash
airflow db migrate
```

### Problème: Clé API invalide

- Vérifiez que `.env` contient la bonne clé
- Attendez quelques minutes si la clé vient d'être créée

### Problème: Port 8080 déjà utilisé

```bash
airflow webserver --port 8081
```

### Voir les logs en temps réel

```bash
tail -f logs/dag_id=openweather_etl_pipeline/.../*.log
```

---

## 📦 Structure des Fichiers

```
airflow_project-1/
├── dags/
│   └── etl.py              ← Pipeline ETL principal
├── .env                     ← Votre configuration (à créer)
├── .env.example            ← Template de configuration
├── requirements.txt        ← Dépendances Python
├── setup.bat/setup.sh      ← Scripts d'installation
├── view_database.py        ← Utilitaire de consultation
└── README.md               ← Documentation complète
```

---

## ✅ Checklist de Livraison

- [ ] Projet compressé (Nom_Prenom.zip)
- [ ] Screenshot de l'UI Airflow (DAG view)
- [ ] Screenshot des logs Extract
- [ ] Screenshot des logs Transform
- [ ] Screenshot des logs Load
- [ ] Screenshot de la base SQLite avec données

---

Pour plus de détails, consultez [README.md](README.md)
