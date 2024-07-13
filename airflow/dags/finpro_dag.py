from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

import requests
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 11),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'finpro_climate',
    default_args=default_args,
    description='Data pipeline DAG',
    schedule_interval=timedelta(days=1),  # Adjust as needed
)

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 13),
    'email_on_failure': False,
    'email_on_retry': False,
}

# Define the DAG
dag = DAG(
    'fetch_coordinates',
    default_args=default_args,
    description='finpro_dag',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Task to fetch coordinates from PostgreSQL
get_coordinates = SQLExecuteQueryOperator(
    task_id='fetch_coordinates',
    conn_id='finpro_climate',
    sql='SELECT lat, long FROM stationlocation;',
    dag=dag,
)

# Task to process the fetched coordinates
process_coordinates_task = PythonOperator(
    task_id='preprocessing_coordinates',
    python_callable=process_coordinates,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
get_coordinates >> process_coordinates_task
