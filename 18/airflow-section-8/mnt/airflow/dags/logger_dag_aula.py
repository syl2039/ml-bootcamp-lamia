# Importações necessárias
import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

default_args = { # Argumentos padrões
        "owner": "airflow", # Nome do dono
        "start_date": airflow.utils.dates.days_ago(1) # Define data de início para o dia anterior
    }
# Cria uma DAG que vai ser executada diariamente
with DAG(dag_id="logger_dag", default_args=default_args, schedule_interval="@daily") as dag:
    # Tarefa ficticia
    t1 = DummyOperator(task_id="t1")
    # Tarefa que pausa a execução por 10 sgeundos
    t2 = BashOperator(
            task_id="t2", # id da tarefa
            bash_command="sleep 10" # Comando bash
        )

    # Fluxo de execução
    t1 >> t2