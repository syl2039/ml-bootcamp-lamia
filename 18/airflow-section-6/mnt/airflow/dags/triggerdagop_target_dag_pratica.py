# Importações necessárias
import airflow.utils.dates
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Informações gerais
# - Adicionei um fluxo de execução
# - Removi a tarefa 3
# - Removi o schedule_interval=None

# Resultados
# Funcionou da mesma maneira, com a única diferença sendo
# que agora foi de forma sequencial e não paralela, achei que
# talvez desse erro com a remoção do schedule_interval mas o valor 
# padrão quando não passado é o None (mesmo de antes)


default_args = { # Argumentos padrões
    'owner': 'Airflow', # Nome do dono
    'start_date': airflow.utils.dates.days_ago(1), # Data de início (1 dia atrás)
}


def remote_value(**context):
    # printa a mensagem no log
    print("Value {} for key=message received from the controller DAG".format(context["dag_run"].conf["message"]))

# Cria uma DAG
with DAG(dag_id="triggerdagop_target_dag", default_args=default_args) as dag:

    # tarefa que imprime a mensagem passada do controlador no log
    t1 = PythonOperator(
            task_id="t1", # id da tarefa
            provide_context=True, # Passa o contexto
            python_callable=remote_value, # chama a função
        )

    # tarefa que imprime a mensagem passada do controlador no terminal
    t2 = BashOperator(
        task_id="t2", # id da tarefa
        bash_command='echo Message: {{ dag_run.conf["message"] if dag_run else "" }}') # Comando bash que printa a mensagem

    # Fluxo de execução
    t1 >> t2