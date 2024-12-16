# Importações necessárias
import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# Informações gerais
# - Troquei o schedule_interval para 10 segundos 
# - Troquei o sleep para 2 segundos
# - Adicionei uma nova tarefa que printa uma mensagem e depois coloquei ela no fluxo de execucao

# Resultados
# Funcionou certinho, a cada dez segundos printava uma mensagem e pausava por dois segundos.
default_args = { # Argumentos padrões
        "owner": "airflow", # Nome do dono
        "start_date": airflow.utils.dates.days_ago(1) # Define data de início para o dia anterior
    }

# Cria uma DAG que vai ser executada diariamente
with DAG(dag_id="logger_dag", default_args=default_args, schedule_interval=timedelta(seconds=10)) as dag:
    # Tarefa ficticia
    t1 = DummyOperator(task_id="t1")
    # Tarefa que pausa a execução por 10 sgeundos
    t2 = BashOperator(
            task_id="t2", # id da tarefa
            bash_command="sleep 2" # Comando bash
        )
    t3 = BashOperator(
            task_id="t3", # id da tarefa
            bash_command="echo 'teste'" # Comando bash
        )
    # Fluxo de execução
    t1 >> t3 >> t2