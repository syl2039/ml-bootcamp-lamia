# Importações necessárias
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = { # Argumentos padrões
    'start_date': datetime(2019, 1, 1), # Data de início
    'owner': 'Airflow', # Nome do dono
    'email': 'owner@test.com' # Email do dono
}

# Criação da dag
# dag_id -> id da DAG
# schedule_interval -> Define a cada quanto tempo vai ser executada
# default_args -> Argumentos padrões definidos acima
# catchup -> Define se a DAG vai tentar recuperar execuções passadas que foram perdidas
with DAG(dag_id='queue_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # Tarefas que precisam de workers com alta capacidade de ler e escrever no ssd
    t_1_ssd = BashOperator(task_id='t_1_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')
    t_2_ssd = BashOperator(task_id='t_2_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')
    t_3_ssd = BashOperator(task_id='t_3_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')

    # Tarefas que exigem um alto desempenho da cpu
    t_4_cpu = BashOperator(task_id='t_4_cpu', bash_command='echo "CPU instensive task"', queue='worker_cpu')
    t_5_cpu = BashOperator(task_id='t_5_cpu', bash_command='echo "CPU instensive task"', queue='worker_cpu')

    # Tarefa que precisa de workers com as dependencias do spark
    t_6_spark = BashOperator(task_id='t_6_spark', bash_command='echo "Spark dependency task"', queue='worker_spark')

    # Tarefa ficticia
    task_7 = DummyOperator(task_id='task_7')

    # A tarefas podem ser executadas paralelamente, e quando todas forem concluidas a sete será acionada
    [t_1_ssd, t_2_ssd, t_3_ssd, t_4_cpu, t_5_cpu, t_6_spark] >> task_7
        