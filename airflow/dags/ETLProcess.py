from airflow import DAG
from airflow.operators.python_operator import PythonOperator
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
    'etl_data_dag',
    default_args=default_args,
    description='ETL process for data from API',
    schedule_interval=timedelta(days=1),  # Adjust as needed
)

def etl_process(**kwargs):
    # Assuming some ETL processing logic here
    data = kwargs['ti'].xcom_pull(task_ids='collect_data_from_api')
    # Perform ETL operations (transformations, cleaning, etc.)
    transformed_data = data  # Replace with actual ETL logic
    return transformed_data

etl_process_task = PythonOperator(
    task_id='etl_process',
    python_callable=etl_process,
    provide_context=True,
    dag=dag,
)

etl_process_task
