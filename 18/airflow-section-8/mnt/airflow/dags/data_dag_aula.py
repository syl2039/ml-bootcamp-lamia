# Importações necessárias
import pprint as pp
import airflow.utils.dates
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

default_args = { # Argumentos padrões
        "owner": "airflow",  # Nome do dono
        "start_date": airflow.utils.dates.days_ago(10), # Define data de início para dez dias atrás
    }
# Cria uma DAG que vai ser executada diariamente
with DAG(dag_id="data_dag", default_args=default_args, schedule_interval="@daily") as dag:
    # Tarefa ficticia
    upload = DummyOperator(task_id="upload")

    # Tarefa que printa uma mensagem
    process = BashOperator(
            task_id="process", # id da tarefa
            bash_command="echo 'processing'" # Comando bash
        )

    # Tarefa que executa um comando bash
    fail = BashOperator(
            task_id="fail", # id da tarefa
            # o comando termina a tarefa com sucesso se o número do dia for par
            # caso for ímpar, ele falha
            bash_command="""
                valid={{macros.ds_format(ds, "%Y-%m-%d", "%d")}}
                if [ $(($valid % 2)) == 1 ]; then
                        exit 1
                else
                        exit 0
                fi
            """
        )

    # Fluxo de execução
    upload >> process >> fail