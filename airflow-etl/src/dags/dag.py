#############
#  IMPORTS  #
#############
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from modules.auth import get_oauth_token
from modules.search import set_url, search_api

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
    schedule_interval="*/2 * * * *",
    catchup=False,
) as dag:
    task1 = PythonOperator(
        task_id="t1_get_oauth_token", python_callable=get_oauth_token,
        provide_context=True
    )
    task2 = PythonOperator(
        task_id="t2_set_url", python_callable=set_url,
        op_kwargs={
                    "country": "es",
                    "operation": "rent",
                    "property_type": "homes"},
        provide_context=True
    )
    task3 = PythonOperator(
        task_id="t3_get_data_from_idealista_api", python_callable=search_api,
        op_kwargs={"pagination": 1},
        provide_context=True
    )

    task1 >> task2 >> task3