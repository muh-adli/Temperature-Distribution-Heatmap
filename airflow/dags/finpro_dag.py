from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta
import requests
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'finpro_climate',
    default_args=default_args,
    description='Finpro Data pipeline DAG',
    schedule_interval=None,
    # schedule_interval='*/30 * * * *',  # Uncomment to run every 30 minutes
    catchup=False,
)

def process_coordinates(ti):
    coordinates = ti.xcom_pull(task_ids='fetching_coordinates')
    if coordinates:
        # Convert the list of tuples with Decimals to a list of lists with floats
        coordinates_array = [[float(coord[0]), float(coord[1])] for coord in coordinates]
        ti.xcom_push(key='coordinates_array', value=coordinates_array)
        logging.info(f"Coordinates fetched: {coordinates_array}")
    else:
        logging.warning("No coordinates fetched.")

def fetch_weather_data(api_key, ti, **kwargs):
    coordinates_array = ti.xcom_pull(task_ids='preprocessing_coordinates', key='coordinates_array')
    
    if not coordinates_array:
        logging.error("No coordinates available for API call.")
        return

    weather_data = []
    for coordinates in coordinates_array:
        # Convert the coordinates to a comma-separated string
        coor_str = f"{coordinates[0]},{coordinates[1]}"
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={coor_str}"
        response = requests.get(url)
        logging.info("fetching url")
        logging.info(url)

        if response.status_code == 200:
            logging.info(f"Successfully collected data for {coor_str}")
            weather_data.append(response.json())
        else:
            logging.error(f"Failed to fetch data for {coor_str}. Status code: {response.status_code}")
    
    logging.info(f"Collected {len(weather_data)} data points.")
    ti.xcom_push(key='weather_data', value=weather_data)

# Task to fetch coordinates from PostgreSQL
get_coordinates = PostgresOperator(
    task_id='fetching_coordinates',
    postgres_conn_id='finpro_climate',
    sql='SELECT lat, long FROM stationlocation;',
    dag=dag,
)

# Task to process the fetched coordinates
process_coordinates_task = PythonOperator(
    task_id='preprocessing_coordinates',
    python_callable=process_coordinates,
    dag=dag,
)

# Task to fetch weather data for the coordinates
fetch_weather_data_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    op_kwargs={'api_key': '692d85fddc6d426aa15121827242806'},
    dag=dag,
)

# Define task dependencies
get_coordinates >> process_coordinates_task >> fetch_weather_data_task
