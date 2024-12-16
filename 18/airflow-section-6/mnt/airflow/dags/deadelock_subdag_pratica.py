# Importações necessárias
import airflow
from subdags.subdag import factory_subdag
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.executors.celery_executor import CeleryExecutor
from airflow.executors.local_executor import LocalExecutor

# Informações gerais
# - Coloquei o id da DAG diretamente
# - Troquei a ordem de fluxo
# - Troquei o executor de duas tarefas
# - Criei mais daus tarefas normais e uma ficticia

# Resultados
# Funcionou normalmente, só que ao invés de executar elas paralelamente
# foi sequencialmente já que o fluxo foi trocado e também agora ao invés
# de dividir em start -> subdags -> final, foi divido em start -> subdags -> meio -> subdags -> final

default_args = { # Argumentos padrões
    'owner': 'Airflow', # Nome do dono
    'start_date': airflow.utils.dates.days_ago(2), # Data de início (dois dias atrás)
}
# Criação de uma dag com o id 'deadlock_subdag', os argumentos padrões que foram definidos lá em cima e ela só vai ser executada uma vez
with DAG(dag_id="deadlock_subdag", default_args=default_args, schedule_interval="@once") as dag:
    # Tarefa ficticia
    start = DummyOperator(
        task_id='start' #Id da tarefa
    )

    subdag_1 = SubDagOperator(
        task_id='subdag-1', #Id da tarefa
        subdag=factory_subdag("deadlock_subdag", 'subdag-1', default_args), # Cria a subdag
        executor=CeleryExecutor() # Executor (esse permite executar em paralelo)
    )

    subdag_2 = SubDagOperator(
        task_id='subdag-2', #Id da tarefa
        subdag=factory_subdag("deadlock_subdag", 'subdag-2', default_args), # Cria a subdag
        executor=CeleryExecutor() # Executor (esse permite executar em paralelo)
    )

    subdag_3 = SubDagOperator(
        task_id='subdag-3', #Id da tarefa
        subdag=factory_subdag("deadlock_subdag", 'subdag-3', default_args), # Cria a subdag
        executor=LocalExecutor() # Executor 
    )

    subdag_4 = SubDagOperator(
        task_id='subdag-4', #Id da tarefa
        subdag=factory_subdag("deadlock_subdag", 'subdag-4', default_args), # Cria a subdag
        executor=LocalExecutor() # Executor 
    )

    # Tarefa ficticia
    meio = DummyOperator(
        task_id='meio' #Id da tarefa
    )

    subdag_5 = SubDagOperator(
        task_id='subdag-5', #Id da tarefa
        subdag=factory_subdag("deadlock_subdag", 'subdag-5', default_args), # Cria a subdag
        executor=LocalExecutor() # Executor 
    )

    subdag_6 = SubDagOperator(
        task_id='subdag-6', #Id da tarefa
        subdag=factory_subdag("deadlock_subdag", 'subdag-6', default_args), # Cria a subdag
        executor=LocalExecutor() # Executor 
    )

    # Tarefa ficticia
    final = DummyOperator(
        task_id='final' #Id da tarefa
    )
    # Fluxo de execução
    start >> subdag_1 >> subdag_2 >> subdag_3 >> subdag_4 >> meio >> subdag_5 >> subdag_6 >> final 