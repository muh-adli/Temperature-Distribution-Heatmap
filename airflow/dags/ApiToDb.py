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
    'data_pipeline_dag',
    default_args=default_args,
    description='Data pipeline DAG',
    schedule_interval=timedelta(days=1),  # Adjust as needed
)

coordinates = [
    [117.81900324660589, 1.266556995789175],
    [117.81470013947921, 1.252922462687],
    [117.82876900112934, 1.25265579383942],
    [117.84661576915529, 1.253043392203096],
    [117.84556899182097, 1.238490146342552],
    [117.85702686424283, 1.221048411955284],
    [117.86419510684932, 1.232452913163146],
    [117.87383321101743, 1.227729700883921],
    [117.8459519716267, 1.213578478390756],
    [117.87019043691407, 1.24202216460154],
    [117.86719956953955, 1.258018896069038],
    [117.88179277229533, 1.267978494572026],
    [117.8902573301201, 1.259846646615722],
    [117.89845832364963, 1.242930426134155],
    [117.89975726100361, 1.231916615344977],
    [117.87932143664251, 1.278992764659367],
    [117.90446061323414, 1.272297296856502],
    [117.91827307994431, 1.284354578251684],
    [117.92816704988338, 1.266913296042288],
    [117.93219810222489, 1.246720855816991],
    [117.91630687808167, 1.249610909462584],
    [117.90745199344171, 1.258660675956391],
    [117.87083205633546, 1.211997181266125]
]

def collect_data_from_api(**kwargs):
    api_key = '692d85fddc6d426aa15121827242806'
    collected_data = []

    for item in coordinates:
        coor_str = f"{item[1]},{item[0]}"
        api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={coor_str}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            collected_data.append(data)
            print(f"Data collected for item {item}:", data)  # Print the collected data for each item
        else:
            print(f"Error collecting data for item {item}. Status code: {response.status_code}")
            # Optionally, you can handle retries or errors here

    # Combine all collected data into one structure if needed
    combined_data = {
        'data': collected_data
    }

    return combined_data

def etl_process(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='collectingAPI')
    # Perform ETL operations (transformations, cleaning, etc.)
    transformed_data = data  # Replace with actual ETL logic
    print("Transformed data:", transformed_data)  # Print the transformed data
    return transformed_data

def insert_data_into_postgres(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='etl_process')
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    table_name = 'dailyClimate'  # Replace with your table name
    rows_to_insert = [(record,) for record in data['data']]  # Adjust this based on your table structure
    pg_hook.insert_rows(table=table_name, rows=rows_to_insert)
    print("Data inserted into PostgreSQL!")  # Print confirmation
    return 'Data inserted successfully into PostgreSQL!'

# Define tasks
collect_data_task = PythonOperator(
    task_id='collectingAPI',
    python_callable=collect_data_from_api,
    provide_context=True,
    dag=dag,
)

etl_process_task = PythonOperator(
    task_id='etl_process',
    python_callable=etl_process,
    provide_context=True,
    dag=dag,
)

insert_data_task = PythonOperator(
    task_id='insert_data_into_postgres',
    python_callable=insert_data_into_postgres,
    provide_context=True,
    dag=dag,
)

# Define task dependencies
collect_data_task >> etl_process_task >> insert_data_task
