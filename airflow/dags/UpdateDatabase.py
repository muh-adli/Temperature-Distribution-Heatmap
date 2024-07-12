from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
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
    'insert_data_dag',
    default_args=default_args,
    description='Insert data into PostgreSQL',
    schedule_interval=timedelta(days=1),  # Adjust as needed
)

def insert_data_into_postgres(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='etl_process')
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    table_name = 'your_table_name'  # Replace with your table name
    pg_hook.insert_rows(table=table_name, rows=data)
    return 'Data inserted successfully into PostgreSQL!'

insert_data_task = PythonOperator(
    task_id='insert_data_into_postgres',
    python_callable=insert_data_into_postgres,
    provide_context=True,
    dag=dag,
)

insert_data_task
