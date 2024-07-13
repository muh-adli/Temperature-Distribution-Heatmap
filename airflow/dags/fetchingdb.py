from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import SQLExecuteQueryOperator
from datetime import datetime, timedelta
import logging

def process_coordinates(ti, **kwargs):
    coordinates = ti.xcom_pull(task_ids='get_coordinates')
    if coordinates:
        # Flatten the list of tuples into a list of coordinates
        coordinates_array = [item for sublist in coordinates for item in sublist]
        # Add your processing logic here
        logging.info(f"Coordinates fetched: {coordinates_array}")
    else:
        logging.warning("No coordinates fetched.")

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,  # No retries for development purposes
}

# Define the DAG
dag = DAG(
    'fetch_and_process_coordinates',
    default_args=default_args,
    description='Test fetch and processing coordinates from PostgreSQL',
    schedule_interval='*/30 * * * *',  # Runs every 30 minutes
    catchup=False,
)

# Task to fetch coordinates from PostgreSQL
get_coordinates = SQLExecuteQueryOperator(
    task_id='get_coordinates',
    conn_id='finpro_climate',  # Make sure this matches the connection ID in Airflow Connections
    sql='SELECT lat, long FROM stationlocation;',
    dag=dag,
)

# Task to process the fetched coordinates
process_coordinates_task = PythonOperator(
    task_id='process_coordinates',
    python_callable=process_coordinates,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
get_coordinates >> process_coordinates_task
