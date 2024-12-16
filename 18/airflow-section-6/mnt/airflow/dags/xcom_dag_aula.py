# importações necessárias
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
from airflow.operators.bash_operator import BashOperator

args = { # Argumentos 
    'owner': 'Airflow', # Nome do dono
    'start_date': airflow.utils.dates.days_ago(1), # Data de início (1 dia atrás)
}

# Retona um string 'my_returned_xcom'
def push_xcom_with_return():
    return 'my_returned_xcom'

# Recebe o contexto e printa
def get_pushed_xcom_with_return(**context):
    print(context['ti'].xcom_pull(task_ids='t0')) 

# define a proxima task, nesse caso é a t3
def push_next_task(**context):
    context['ti'].xcom_push(key='next_task', value='t3')

# Recupera o valor da proxima task
def get_next_task(**context):
    return context['ti'].xcom_pull(key='next_task')

# Pega os xcoms das tarefas t0 e t2 e printa os valores
def get_multiple_xcoms(**context):
    print(context['ti'].xcom_pull(key=None, task_ids=['t0', 't2']))

# Criação de uma dag que vai ser executada uma única vez
with DAG(dag_id='xcom_dag', default_args=args, schedule_interval="@once") as dag:
    
    t0 = PythonOperator(
        task_id='t0', # id da tarefa
        python_callable=push_xcom_with_return # Chama a função
    )

    t1 = PythonOperator(
        task_id='t1', # id da tarefa
        provide_context=True, # Passa o contexto
        python_callable=get_pushed_xcom_with_return # Chama a função
    )

    t2 = PythonOperator(
        task_id='t2', # id da tarefa
        provide_context=True, # Passa o contexto
        python_callable=push_next_task # Chama a função
    )

    branching = BranchPythonOperator(
        task_id='branching', # id da tarefa
        provide_context=True, # Passa o contexto
        python_callable=get_next_task, # Chama a função
    )
    # Tarefa ficticia
    t3 = DummyOperator(task_id='t3')
    # Tarefa ficticia
    t4 = DummyOperator(task_id='t4')

    t5 = PythonOperator(
        task_id='t5', # id da tarefa
        trigger_rule='one_success', # é executada assim que umas das anteriores for bem sucedida
        provide_context=True, # Passa o contexto
        python_callable=get_multiple_xcoms # Chama a função
    )

    t6 = BashOperator(
        task_id='t6', # id da tarefa
        bash_command="echo value from xcom: {{ ti.xcom_pull(key='next_task') }}" # Comando bash
    )

    # Fluxo de execução
    t0 >> t1
    t1 >> t2 >> branching
    branching >> t3 >> t5 >> t6
    branching >> t4 >> t5 >> t6