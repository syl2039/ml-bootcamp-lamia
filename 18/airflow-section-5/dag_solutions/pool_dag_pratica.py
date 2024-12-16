# Importações necessárias
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# Informações gerais
# - Troquei o catchup para True
# - Removi as dependencias da linha 85
# - Troquei o xcom_push de uma tarefa para falso 
# - Troquei uma prioridade para zero
# - Troquei a data de inicio para 2024
# - Troquei o schedule_interval para ser mensal
# - Troquei um endpoint para um inexistente

# Resultados
# Como o catchup foi setado como True, todas as tarefas não executadas mensalmentes 
# desde a data de incio foram executadas, a tarefa que o xcom_push foi definido para
# falso não armazenou os valores, a tarefa com a prioridade zero foi sempre a ultima
# a ser executada, e a que o endpoint não existe dava erro porque não encontrava o 
# caminho, como as dependencias foram removidas, a ultima tarefa printou normalmente
# os resultados, mas a única que dava certo foi a do dólar.


default_args = { # Definição dos argumentos padrões
    'start_date': datetime(2024, 1, 1), # Data inicial
    'owner': 'Airflow', # Nome do dono
    'email': 'owner@test.com' # Email do dono
}
# Criação da dag
# dag_id -> id da DAG
# schedule_interval -> Define a cada quanto tempo vai ser executada
# default_args -> Argumentos padrões definidos acima
# catchup -> Define se a DAG vai tentar recuperar execuções passadas que foram perdidas
with DAG(dag_id='pool_dag', schedule_interval='0 0 1 * *', default_args=default_args, catchup=True) as dag:
    
    # Tarefa pra pegar as taxas de cambio para EUR 
    get_forex_rate_EUR = SimpleHttpOperator( 
        task_id='get_forex_rate_EUR', # id da tarefa                                                                
        method='GET', # Método HTTP (Get)                                  
        priority_weight=1, # Prioridade da tarefa                                   
        pool='forex_api_pool', # Limita o número de tarefas dentro de um pool
        http_conn_id='forex_api', # Conexão para acessar a API                           
        endpoint='/latest?base=EUR', # Caminho para obter as taxas                          
        xcom_push= False # Não permite o xcom (comunicação entre as tarefas)               
    )
 
    ## Tarefa pra pegar as taxas de cambio para USD 
    get_forex_rate_USD = SimpleHttpOperator(
        task_id='get_forex_rate_USD', # id da tarefa                                                                
        method='GET', # Método HTTP (Get)
        priority_weight= 0,  # Prioridade da tarefa                                   
        pool='forex_api_pool', # Limita o número de tarefas dentro de um pool
        http_conn_id='forex_api', # Conexão para acessar a API   
        endpoint='/latest?base=USD', # Caminho para obter as taxas  
        xcom_push=True # Permite o xcom (comunicação entre as tarefas)    
    )
 
    # Tarefa pra pegar as taxas de cambio para JPY 
    get_forex_rate_JPY = SimpleHttpOperator(
        task_id='get_forex_rate_JPY', # id da tarefa                                                                
        method='GET', # Método HTTP (Get)
        priority_weight=3, # Prioridade da tarefa                                   
        pool='forex_api_pool', # Limita o número de tarefas dentro de um pool
        http_conn_id='forex_api', # Conexão para acessar a API   
        endpoint='/latest?base=naoexiste', # Caminho para obter as taxas  
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
    # [get_forex_rate_EUR, get_forex_rate_USD, get_forex_rate_JPY] >> show_data