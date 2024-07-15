#!/bin/bash

# Database connection parameters
host="localhost"  # Replace with your PostgreSQL host
port="5432"       # PostgreSQL default port
database="weather"
user="airflow"
password="airflow"  # Replace with your password

# Loop to generate and insert random data
start_timestamp="2024-07-14 20:00:00"
end_timestamp="2024-07-15 20:00:00"
current_timestamp="$start_timestamp"
interval="30 minutes"

while [ "$current_timestamp" \< "$end_timestamp" ]; do
    idloc=$((RANDOM % 10 + 1))
    tempc=$(awk -v min=20.0 -v max=35.0 'BEGIN{srand(); print min+rand()*(max-min)}')
    windkph=$(awk -v min=0.0 -v max=50.0 'BEGIN{srand(); print min+rand()*(max-min)}')
    winddeg=$((RANDOM % 360))
    pressmb=$(awk -v min=1000.0 -v max=1020.0 'BEGIN{srand(); print min+rand()*(max-min)}')
    hum=$((RANDOM % 41 + 50))  # Random number between 50 and 90
    uv=$(awk -v min=0.0 -v max=10.0 'BEGIN{srand(); print min+rand()*(max-min)}')

    # Constructing the INSERT statement
    insert_statement="INSERT INTO public.dailyclimate (idloc, tempc, windkph, winddeg, pressmb, hum, uv, timestamp) VALUES ($idloc, $tempc, $windkph, $winddeg, $pressmb, $hum, $uv, '$current_timestamp');"

    # Insert data using psql
    echo "Executing: $insert_statement"
    PGPASSWORD="$password" psql -h "$host" -p "$port" -U "$user" -d "$database" -c "$insert_statement"

    # Move to the next timestamp (30 minutes interval)
    current_timestamp=$(date -d "$current_timestamp $interval" +"%Y-%m-%d %H:%M:%S")
done
