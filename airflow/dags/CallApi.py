from airflow import DAG
from airflow.operators.python_operator import PythonOperator
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
    'collect_data_dag',
    default_args=default_args,
    description='Collect data from API',
    schedule_interval=timedelta(days=1),  # Adjust as needed
)

def collect_data_from_api(**kwargs):
    api_url = 'https://api.example.com/data'  # Replace with your API endpoint
    response = requests.get(api_url)
    data = response.json()
    return data

collect_data_task = PythonOperator(
    task_id='collect_data_from_api',
    python_callable=collect_data_from_api,
    provide_context=True,
    dag=dag,
)

collect_data_task
