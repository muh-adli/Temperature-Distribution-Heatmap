from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from datetime import datetime, timedelta
import requests
import logging
import json

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
    schedule_interval='*/30 * * * *',
    catchup=False,
)

def process_coordinates(ti):
    coordinates = ti.xcom_pull(task_ids='fetching_postgres')
    if coordinates:
        processed_coordinates = []
        for coord in coordinates:
            if len(coord) == 4:
                processed_coordinates.append([float(coord[0]), float(coord[1]), coord[2], coord[3]])
            else:
                logging.error(f"Unexpected coordinate format: {coord}")
        ti.xcom_push(key='coordinates_array', value=processed_coordinates)
        # logging.info(f"Processed coordinates: {processed_coordinates}")
    else:
        logging.error("Station coordinates not fetched.")

def fetch_weather_data(api_key, ti):
    coordinates_array = ti.xcom_pull(task_ids='preprocessing', key='coordinates_array')
    
    if not coordinates_array:
        logging.error("Error! No coordinates available.")
        return

    weather_data = {}
    for coordinates in coordinates_array:
        try:
            stationId = coordinates[2]
            stationName = coordinates[3]
            coor_str = f"{coordinates[0]},{coordinates[1]}"
            url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={coor_str}"
            response = requests.get(url)
            print("fetching url on", str(stationName), "Id", str(stationId))
            
            if response.status_code == 200:
                logging.info(f"Successfully connected to API on {stationName}")
                data = response.json()
                if 'current' in data:
                    current_weather = data['current']
                    weather_info = {
                        "station_id": stationId,
                        "station_name": stationName,
                        "temp_c": current_weather.get("temp_c"),
                        "wind_kph": current_weather.get("wind_kph"),
                        "wind_degree": current_weather.get("wind_degree"),
                        "pressure_mb": current_weather.get("pressure_mb"),
                        "humidity": current_weather.get("humidity"),
                        "uv": current_weather.get("uv"),
                        "timestamp": current_weather.get("last_updated")
                        }
                    weather_data[stationId] = weather_info

                    logging.info(f"Data collected at {current_weather['last_updated']}")
                    print("----------------------------------------------------------")
                    print(weather_info)
                    print("----------------------------------------------------------")
                else:
                    logging.error(f"Error on {coor_str}. Missing 'current' key.")
            else:
                logging.error(f"Failed to fetch data for {coor_str}. Status code: {response.status_code}")
            logging.info("========================================")
        except IndexError as e:
            logging.error(f"Error processing coordinates {coordinates}: {e}")

    logging.info(f"Collected {len(weather_data)} data points.")
    print("=====================================================")
    weather_data_json = json.dumps(weather_data)
    print(weather_data_json)
    ti.xcom_push(key='weather_data', value=weather_data_json)

def insert_weather_data(ti):
    weather_data_json = ti.xcom_pull(task_ids='fetch_API', key='weather_data')
    
    if not weather_data_json:
        logging.error("No weather data available.")
        return

    weather_data = json.loads(weather_data_json)
    # logging.info(f"Weather data to be inserted: {weather_data}")
    insert_sql = """
    INSERT INTO dailyclimate (idloc, tempc, windkph, winddeg, pressmb, hum, uv, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    logging.info(f"Executing SQL: {insert_sql}")
    pg_hook = PostgresHook(postgres_conn_id='finpro_climate')

    for station_id, weather_info in weather_data.items():
        check_sql = """
        SELECT COUNT(*) FROM dailyclimate WHERE idloc = %s AND timestamp = %s
        """
        check_params = (weather_info['station_id'], weather_info['timestamp'])
        
        records = pg_hook.get_first(sql=check_sql, parameters=check_params)
        
        if records[0] == 0:
            values = (
                weather_info['station_id'],
                weather_info['temp_c'],
                weather_info['wind_kph'],
                weather_info['wind_degree'],
                weather_info['pressure_mb'],
                weather_info['humidity'],
                weather_info['uv'],
                weather_info['timestamp']
            )

            logging.info(f"With parameters: {values}")
            pg_hook.run(insert_sql, parameters=values)
            logging.info(f"Inserted weather data for station ID: {station_id}")
        else:
            logging.info(f"Record already exists for station ID: {station_id} at timestamp: {weather_info['timestamp']}")

## DAG Task

get_coor = PostgresOperator(
    task_id='fetching_postgres',
    postgres_conn_id='finpro_climate',
    sql='SELECT lat, long, id, name FROM stationlocation;',
    dag=dag,
)

process_coor = PythonOperator(
    task_id='preprocessing',
    python_callable=process_coordinates,
    provide_context=True,
    dag=dag,
)

fetch_weather = PythonOperator(
    task_id='fetch_API',
    python_callable=fetch_weather_data,
    op_kwargs={'api_key': '692d85fddc6d426aa15121827242806'},
    provide_context=True,
    dag=dag,
)

insert_postgres = PythonOperator(
    task_id='insert_postgres',
    python_callable=insert_weather_data,
    provide_context=True,
    dag=dag,
)

get_coor >> process_coor >> fetch_weather >> insert_postgres
