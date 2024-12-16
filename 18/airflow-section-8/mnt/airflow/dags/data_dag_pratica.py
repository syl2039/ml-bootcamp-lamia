# Importações necessárias
import pprint as pp
import airflow.utils.dates
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# Informações gerais
# - Adicionei mais uma tarefa para pausa a exeução
# - Adicionei comandos para informar o usuário quando a tarefa falhar ou passar
# - Adicionei a nova tarefa no fluxo de execução
# - Troquei para verificar o mês ao invés do dia
# - Troque o intervalo mas mensal ao invés de diário

# Resultados
# Executou normalmente com a nova tarefa, verificou certinho o mês e 
# informou diretamente ao usuáiro se passou ou se falhou

default_args = { # Argumentos padrões
        "owner": "airflow",  # Nome do dono
        "start_date": airflow.utils.dates.days_ago(10), # Define data de início para dez dias atrás
    }
# Cria uma DAG que vai ser executada diariamente
with DAG(dag_id="data_dag", default_args=default_args, schedule_interval="@monthly") as dag:
    # Tarefa ficticia
    upload = DummyOperator(task_id="upload")

    # Tarefa que printa uma mensagem
    process = BashOperator(
            task_id="process", # id da tarefa
            bash_command="echo 'processing'" # Comando bash
        )
    
    # Tarefa que pausa a execução por dois segundos
    sleep = BashOperator(
            task_id="sleep", # id da tarefa
            bash_command="sleep 2'" # Comando bash
        )

    # Tarefa que executa um comando bash
    fail = BashOperator(
            task_id="fail", # id da tarefa
            # o comando termina a tarefa com sucesso se o número do dia for par
            # caso for ímpar, ele falha
            bash_command="""
                valid={{macros.ds_format(ds, "%Y-%m-%d", "%m")}}
                if [ $(($valid % 2)) == 1 ]; then
                        echo 'Mes impar, falhou'
                        exit 1
                else
                        echo 'Mes par, passou'
                        exit 0
                fi
            """
        )

    # Fluxo de execução
    upload >> process >> sleep >> fail