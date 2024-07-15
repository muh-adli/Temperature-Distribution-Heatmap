import psycopg2
from psycopg2 import Error
from datetime import datetime, timedelta
import random

# Database connection parameters
host = 'postgres'  # Replace with your Docker container IP or hostname
port = '5432'       # PostgreSQL default port
database = 'weather'
user = 'airflow'
password = 'airflow'  # Replace with your password

try:
    # Connect to PostgreSQL
    connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)

    cursor = connection.cursor()

    # Generate and insert random data for 14th July 20:00 to 15th July 20:00 with 30-minute intervals
    start_timestamp = datetime(2024, 7, 14, 20, 0, 0)
    end_timestamp = datetime(2024, 7, 15, 20, 0, 0)
    current_timestamp = start_timestamp

    while current_timestamp <= end_timestamp:
        idloc = random.randint(1, 10)
        tempc = round(random.uniform(20.0, 35.0), 2)
        windkph = round(random.uniform(0.0, 50.0), 2)
        winddeg = random.randint(0, 360)
        pressmb = round(random.uniform(1000.0, 1020.0), 2)
        hum = random.randint(50, 90)
        uv = round(random.uniform(0.0, 10.0), 1)

        insert_query = """ INSERT INTO public.dailyclimate (idloc, tempc, windkph, winddeg, pressmb, hum, uv, timestamp)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        data_to_insert = (idloc, tempc, windkph, winddeg, pressmb, hum, uv, current_timestamp)

        # Execute the INSERT statement
        # cursor.execute(insert_query, data_to_insert)

        # Move to the next timestamp (30 minutes interval)
        current_timestamp += timedelta(minutes=30)

    connection.commit()
    print("Data inserted successfully")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL or inserting data:", error)

finally:
    # Closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
