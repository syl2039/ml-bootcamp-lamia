# importações necessárias
import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

# Dicionário com as apis
IP_GEOLOCATION_APIS = {
    'ip-api': 'http://ip-api.com/json/',
    'ipstack': 'https://api.ipstack.com/',
    'ipinfo': 'https://ipinfo.io/json'
}

# Função que checa qual se adequa mais
def check_api():
    for api, link in IP_GEOLOCATION_APIS.items():
        r = requests.get(link)
        try:
            data = r.json()
            if data and 'country' in data and len(data['country']):
                return api
        except ValueError:
            pass
    return 'none'
# Criação da dag
with DAG(dag_id='branch_dag', 
    default_args=default_args, 
    schedule_interval="@once") as dag:

    # chamado da função que checa qual se adequa mais
    check_api = BranchPythonOperator(
        task_id='check_api',
        python_callable=check_api
    )
    # Caso nenhuma se adeque cai aqui
    none = DummyOperator(
        task_id='none'
    )
    # Salva a tarefa a se feita
    save = DummyOperator(task_id='save')

    # Fluxo de execução
    check_api >> none >> save

    # Cria tarefas de acordo com a API
    for api in IP_GEOLOCATION_APIS:
        process = DummyOperator(
            task_id=api
        )
        # Fluxo de execução
        check_api >> process >> save