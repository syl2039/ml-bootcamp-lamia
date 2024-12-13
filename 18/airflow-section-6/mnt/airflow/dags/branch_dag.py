# Importações necessárias
import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

default_args = { # Argumentos padrões
    'owner': 'Airflow', # Nome do dono
    'start_date': airflow.utils.dates.days_ago(2), # Data de início (2 dias atrás)
}

IP_GEOLOCATION_APIS = { # Lista com três APIs de geolocalização de IP
    'ip-api': 'http://ip-api.com/json/',
    'ipstack': 'https://api.ipstack.com/',
    'ipinfo': 'https://ipinfo.io/json'
}


def check_api():
    apis = [] # Lista para adicionar as APIs
    for api, link in IP_GEOLOCATION_APIS.items():
        r = requests.get(link)
        try:
            data = r.json() # converte para formato json
            if data and 'country' in data and len(data['country']): # verifica se a chave 'country' existe e se é vazia
                apis.append(api) # Adiciona a lista
        except ValueError: # Se der erro vai cair aqui e não vai fazer nada, só passar 
            pass
    return apis if len(apis) > 0 else 'none' # Se pelo menos uma API corresponder ele passa ela, se não 'none'
# Criação de uma dag com o id 'brach_dag', os argumentos padrões que foram definidos lá em cima e ela só vai ser executada uma vez
with DAG(dag_id='branch_dag', 
    default_args=default_args, 
    schedule_interval="@once") as dag:

    # Tarefa que com base no resultado do python_callable decide qual rumo a DAG vai seguir
    check_api = BranchPythonOperator(
        task_id='check_api', # Id da tarefa
        python_callable=check_api # Chama a função check_api
    )

    # Tarefa ficticia
    none = DummyOperator(
        task_id='none'
    )

    # Tarefa ficticia
    save = DummyOperator(task_id='save', trigger_rule='one_success')

    # Fluxo de execução
    check_api >> none >> save

    # For responsável por criar tarefas dinamicas de acordo com a API
    for api in IP_GEOLOCATION_APIS:
        process = DummyOperator(
            task_id=api
        )
    
        check_api >> process >> save # Fluxo de execução