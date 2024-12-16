# Importações necessárias
import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = { # Argumentos padrões
    'owner': 'Airflow', # Nome do dono
    'start_date': airflow.utils.dates.days_ago(1), # Data de início (1 dia atrás)
}

 # Função que dependendo do resultado aciona a dag
def conditionally_trigger(context, dag_run_obj):
    if context['params']['condition_param']: # Verifica se os parametros são verdadeiros
        dag_run_obj.payload = { # Adiciona os dados ao payload
                'message': context['params']['message']
            }
        pp.pprint(dag_run_obj.payload) # Prita o payload
        return dag_run_obj # Retorna o payload
    
# Criação de uma DAG que só vai ser executada uma vez
with DAG(dag_id="triggerdagop_controller_dag", default_args=default_args, schedule_interval="@once") as dag:
    trigger = TriggerDagRunOperator( # Executor
        task_id="trigger_dag", #id da tarefa
        trigger_dag_id="triggerdagop_target_dag", # DAG que vai ser acionada
        provide_context=True, # Tem que passar o contextp
        python_callable=conditionally_trigger, # Chama a função
        params={
            'condition_param': True, # Define se a outra DAG vai ser executada
            'message': 'Hi from the controller' # Mensagem a ser passada
        },

    )
    # Tarefa ficticia
    last_task = DummyOperator(task_id="last_task")
    # Fluxo de execução
    trigger >> last_task