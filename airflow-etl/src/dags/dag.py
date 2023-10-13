#############
#  IMPORTS  #
#############
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from modules.auth import get_oauth_token

#############
#    DAG    #
#############

default_args = {
    "owner": "Jorge Tarancon;Roberto Hernandez",
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="dag_idealista_api_to_db",
    default_args=default_args,
    start_date=datetime(2023, 10, 13),
    schedule_interval="* * * * *",
    catchup=False,
) as dag:
    task1 = PythonOperator(
        task_id="get_oauth_token", python_callable=get_oauth_token
    )
#    task2 = PythonOperator(
#        task_id="get_data_from_idealista_api", python_callable=
#    )
#    task3 = PythonOperator(
#        task_id="transform_data", python_callable=
#    )
#    task4 = PythonOperator(
#        task_id="upload_data_to_db", python_callable=
#    )

    task1