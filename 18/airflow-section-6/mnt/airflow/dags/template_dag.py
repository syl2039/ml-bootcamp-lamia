# Importações necessárias

import sys
import airflow
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta
from process_logs import process_logs_func

# Insere um novo PATH no sistema
sys.path.insert(1, '/usr/local/airflow/dags/scripts')


# Template de diretório de logs
TEMPLATED_LOG_DIR = """{{ var.value.source_path }}/data/{{ macros.ds_format(ts_nodash, "%Y%m%dT%H%M%S", "%Y-%m-%d-%H-%M") }}/"""

default_args = { # Argumentos padrões
            "owner": "Airflow", # Nome do dono
            "start_date": airflow.utils.dates.days_ago(1), # Data de início (dia anterior)
            "depends_on_past": False, # Dependencia nas execuções anteriores
            "email_on_failure": False, # Notificação quando falhar
            "email_on_retry": False, # Notificação quando tentar de novo
            "email": "youremail@host.com", # Email do dono
            "retries": 1 # Número de retentativas
        }
# Criação da DAG com o id "template_dag", que vai ser executada diariamente com os argumentos padrões
with DAG(dag_id="template_dag", schedule_interval="@daily", default_args=default_args) as dag:
        
        # Printa o timestamp sem formatação e com
        t0 = BashOperator(
            task_id="t0", # Id da tarefa
            bash_command="echo {{ ts_nodash }} - {{ macros.ds_format(ts_nodash, '%Y%m%dT%H%M%S', '%Y-%m-%d-%H-%M') }}") # Comando que vai ser executado

        # Cria um novo log
        t1 = BashOperator(
            task_id="generate_new_logs", # Id da tarefa
            bash_command="./scripts/generate_new_logs.sh", # Comando que vai ser executado
            params={'filename': 'log.csv'}) # Parametros

        # Verifica se o log já existe
        t2 = BashOperator(
            task_id="logs_exist", # Id da tarefa
            bash_command="test -f " + TEMPLATED_LOG_DIR + "log.csv", # Comando que vai ser executado
            )
        # chama a função process_logs_func passando os dados
        t3 = PythonOperator(
            task_id="process_logs", # Id da tarefa
            python_callable=process_logs_func, # Função que vai ser chamada
            templates_dict={'log_dir': TEMPLATED_LOG_DIR}, # passa o template junto
            params={'filename': 'log.csv'} # Parametros
            )

        t0 >> t1 >> t2 >> t3 # Fluxo de execução