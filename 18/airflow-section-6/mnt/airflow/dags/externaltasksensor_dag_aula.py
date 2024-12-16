# importações necessárias
import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

default_args = { # Argumentos padrões
        "owner": "airflow", # Nome do dono 
        "start_date": airflow.utils.dates.days_ago(1) # Tempo de início (um dia atrás)
    }
# Cria uma dag com os argumentos padrões que vai ser executada diarimente
with DAG(dag_id="externaltasksensor_dag", default_args=default_args, schedule_interval="@daily") as dag:
    sensor = ExternalTaskSensor(
        task_id='sensor', # ida da tarefa
        external_dag_id='sleep_dag', # id da DAG externa
        external_task_id='t2' # id da tarefa externa   
    )

    # tarefa ficticia
    last_task = DummyOperator(task_id="last_task")

    # fluxo de execução
    sensor >> last_task