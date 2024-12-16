# Importações necessárias
import airflow
from subdags.subdag import factory_subdag
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.executors.celery_executor import CeleryExecutor

DAG_NAME="deadlock_subdag" # id da DAG

default_args = { # Argumentos padrões
    'owner': 'Airflow', # Nome do dono
    'start_date': airflow.utils.dates.days_ago(2), # Data de início (dois dias atrás)
}
# Criação de uma dag com o id 'deadlock_subdag', os argumentos padrões que foram definidos lá em cima e ela só vai ser executada uma vez
with DAG(dag_id=DAG_NAME, default_args=default_args, schedule_interval="@once") as dag:
    # Tarefa ficticia
    start = DummyOperator(
        task_id='start' #Id da tarefa
    )

    subdag_1 = SubDagOperator(
        task_id='subdag-1', #Id da tarefa
        subdag=factory_subdag(DAG_NAME, 'subdag-1', default_args), # Cria a subdag
        executor=CeleryExecutor() # Executor (esse permite executar em paralelo)
    )

    subdag_2 = SubDagOperator(
        task_id='subdag-2', #Id da tarefa
        subdag=factory_subdag(DAG_NAME, 'subdag-2', default_args), # Cria a subdag
        executor=CeleryExecutor() # Executor (esse permite executar em paralelo)
    )

    subdag_3 = SubDagOperator(
        task_id='subdag-3', #Id da tarefa
        subdag=factory_subdag(DAG_NAME, 'subdag-3', default_args), # Cria a subdag
        executor=CeleryExecutor() # Executor (esse permite executar em paralelo)
    )

    subdag_4 = SubDagOperator(
        task_id='subdag-4', #Id da tarefa
        subdag=factory_subdag(DAG_NAME, 'subdag-4', default_args), # Cria a subdag
        executor=CeleryExecutor() # Executor (esse permite executar em paralelo)
    )

    final = DummyOperator(
        task_id='final' #Id da tarefa
    )

    # Fluxo de execução
    start >> [subdag_1, subdag_2, subdag_3, subdag_4] >> final