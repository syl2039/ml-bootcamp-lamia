# Importações necessárias
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = { # Definição dos argumentos padrões
    'start_date': datetime(2019, 1, 1), # Data inicial
    'owner': 'Airflow', # Nome do dono
    'email': 'owner@test.com' # Email do dono
}
# Criação da dag
# dag_id -> id da DAG
# schedule_interval -> Define a cada quanto tempo vai ser executada
# default_args -> Argumentos padrões definidos acima
# catchup -> Define se a DAG vai tentar recuperar execuções passadas que foram perdidas
with DAG(dag_id='pool_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # Tarefa pra pegar as taxas de cambio para EUR 
    get_forex_rate_EUR = SimpleHttpOperator( 
        task_id='get_forex_rate_EUR', # id da tarefa                                                                
        method='GET', # Método HTTP (Get)                                  
        priority_weight=1, # Prioridade da tarefa                                   
        pool='forex_api_pool', # Limita o número de tarefas dentro de um pool
        http_conn_id='forex_api', # Conexão para acessar a API                           
        endpoint='/latest?base=EUR', # Caminho para obter as taxas                          
        xcom_push=True # Permite o xcom (comunicação entre as tarefas)               
    )
 
    # get forex rates of JPY and push them into XCOM
    get_forex_rate_USD = SimpleHttpOperator(
        task_id='get_forex_rate_USD', # id da tarefa                                                                
        method='GET', # Método HTTP (Get)
        priority_weight=2,  # Prioridade da tarefa                                   
        pool='forex_api_pool', # Limita o número de tarefas dentro de um pool
        http_conn_id='forex_api', # Conexão para acessar a API   
        endpoint='/latest?base=USD', # Caminho para obter as taxas  
        xcom_push=True # Permite o xcom (comunicação entre as tarefas)    
    )
 
    # get forex rates of JPY and push them into XCOM
    get_forex_rate_JPY = SimpleHttpOperator(
        task_id='get_forex_rate_JPY', # id da tarefa                                                                
        method='GET', # Método HTTP (Get)
        priority_weight=3, # Prioridade da tarefa                                   
        pool='forex_api_pool', # Limita o número de tarefas dentro de um pool
        http_conn_id='forex_api', # Conexão para acessar a API   
        endpoint='/latest?base=JPY', # Caminho para obter as taxas  
        xcom_push=True # Permite o xcom (comunicação entre as tarefas)    
    )
 
   # Cmando que vai ser executado
   # Consiste em um for que vai percorrer as tasks e printar os valores
    bash_command="""
        {% for task in dag.task_ids %} 
            echo "{{ task }}"
            echo "{{ ti.xcom_pull(task) }}"
        {% endfor %}
    """

    # Exibe os resultados chamando o comando bash
    show_data = BashOperator(
        task_id='show_result',
        bash_command=bash_command
    )
    # Define uma dependencia pro show_data, antes dele ser executado as outras tres tarefas tem que ser executadas
    [get_forex_rate_EUR, get_forex_rate_USD, get_forex_rate_JPY] >> show_data