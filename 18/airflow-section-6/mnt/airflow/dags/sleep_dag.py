# Importações necessárias
import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

default_args = { # Argumentos padrões
        "owner": "airflow", # Nome do dono 
        "start_date": airflow.utils.dates.days_ago(1) # Tempo de início (um dia atrás)
    }
# Cria a DAG com os argumentos padrões que vai ser executada diariamente
with DAG(dag_id="sleep_dag", default_args=default_args, schedule_interval="@daily") as dag:

    # Tarefa ficticia
    t1 = DummyOperator(task_id="t1")

    # Tarefa que executa um comando bash que pausa por 30 segundos
    t2 = BashOperator(
            task_id="t2", # id da tarefa
            bash_command="sleep 30" # comando
        )
    
    # fluxo de execução
    t1 >> t2