.mode column
.headers on
.width 5 15 8 10 10 8 8 25 20

SELECT 
    id,
    city,
    country,
    temperature_celsius AS temp_c,
    humidity,
    wind_speed_kmh AS wind,
    temperature_category AS category,
    weather_description AS weather,
    date_time
FROM weather_data
ORDER BY id DESC
LIMIT 10;

-- ================================================
.print "\n=========================================="
.print "STATISTIQUES MÉTÉO"
.print "==========================================\n"

SELECT 
    COUNT(*) AS total_records,
    ROUND(AVG(temperature_celsius), 2) AS avg_temp_celsius,
    ROUND(MIN(temperature_celsius), 2) AS min_temp_celsius,
    ROUND(MAX(temperature_celsius), 2) AS max_temp_celsius,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(AVG(wind_speed_kmh), 2) AS avg_wind_kmh
FROM weather_data;



.print "RÉPARTITION PAR CATÉGORIE DE TEMPÉRATURE"

SELECT 
    temperature_category,
    COUNT(*) AS count,
    ROUND(AVG(temperature_celsius), 2) AS avg_temp
FROM weather_data
GROUP BY temperature_category
ORDER BY count DESC;


.print "ENREGISTREMENTS RÉCENTS"


SELECT 
    city,
    temperature_celsius,
    feels_like_celsius,
    humidity,
    weather_description,
    date_time
FROM weather_data
WHERE datetime(created_at) >= datetime('now', '-1 day')
ORDER BY created_at DESC;


.print "STRUCTURE DE LA TABLE"


.schema weather_data

-- ================================================
-- 6. EXPORT CSV (décommentez pour exporter)
-- ================================================
.mode csv
.output weather_export.csv
SELECT * FROM weather_data;
.output stdout
.mode column
