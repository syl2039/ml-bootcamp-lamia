# importações necessárias
import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# Informações gerais
# - ao chamar a dag externa, passei somente a dag e não a tarefa
# - ao invés de chamar a dag sleep_dag, chamei a sleep_dag_teste porque
# a sleep_dag tem um fluxo de execução então mesmo que eu só chamasse uma 
# tarefa específica ele ia ter que executara a dag inteira, então o teste
# de chamar só a dag e não passar a tarefa não faria sentido

# Resultados
# Executou a dag inteira

default_args = { # Argumentos padrões
        "owner": "airflow", # Nome do dono 
        "start_date": airflow.utils.dates.days_ago(1) # Tempo de início (um dia atrás)
    }
# Cria uma dag com os argumentos padrões que vai ser executada diarimente
with DAG(dag_id="externaltasksensor_dag", default_args=default_args, schedule_interval="@daily") as dag:
    sensor = ExternalTaskSensor(
        task_id='sensor', # ida da tarefa
        external_dag_id='sleep_dag', # id da DAG externa
    )

    # tarefa ficticia
    last_task = DummyOperator(task_id="last_task")

    # fluxo de execução
    sensor >> last_task