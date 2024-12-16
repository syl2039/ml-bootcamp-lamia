# Importações necessárias
import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

default_args = { # Argumentos padrões
    'owner': 'Airflow', # Nome do dono
    'start_date': airflow.utils.dates.days_ago(1), # Data de início (um dia atrás)
}

# As funções abaixo só simulam as tarefas pra fazer o desafio passado no curso 
def download_website_a():
    print("download_website_a")
    #raise ValueError("error")
def download_website_b():
    print("download_website_b")
    #raise ValueError("error")
def download_failed():
    print("download_failed")
    #raise ValueError("error")
def download_succeed():
    print("download_succeed")
    #raise ValueError("error")
def process():
    print("process")
    #raise ValueError("error")
def notif_a():
    print("notif_a")
    #raise ValueError("error")
def notif_b():
    print("notif_b")
    #raise ValueError("error")

# Criação de uma dag com o id 'trigger_rule_dag', os argumentos padrões que foram definidos lá em cima e ela só vai ser executada uma vez ao dia
with DAG(dag_id='trigger_rule_dag', 
    default_args=default_args, 
    schedule_interval="@daily") as dag:

    download_website_a_task = PythonOperator(
        task_id='download_website_a', # Id da tarefa
        python_callable=download_website_a, # Chama a função
        trigger_rule="all_success" # Define condição, nesse caso só vai rodas se as anteriores foram sucesso
    ) 

    download_website_b_task = PythonOperator(
        task_id='download_website_b', # Id da tarefa
        python_callable=download_website_b, # Chama a função
        trigger_rule="all_success" # Define condição, nesse caso só vai rodas se as anteriores foram sucesso    
    )

    download_failed_task = PythonOperator(
        task_id='download_failed', # Id da tarefa
        python_callable=download_failed, # Chama a função
        trigger_rule="all_failed" # Define condição, nesse caso só vai rodar se as anteriores falharam
    )

    download_succeed_task = PythonOperator(
        task_id='download_succeed', # Id da tarefa
        python_callable=download_succeed, # Chama a função
        trigger_rule="all_success" # Define condição, nesse caso só vai rodas se as anteriores foram sucesso
    )

    process_task = PythonOperator(
        task_id='process', # Id da tarefa
        python_callable=process, # Chama a função
        trigger_rule="one_success" # Define condição, nesse caso só vai rodar se ao menos uma foi sucesso
    )

    notif_a_task = PythonOperator(
        task_id='notif_a', # Id da tarefa
        python_callable=notif_a, # Chama a função
        trigger_rule="none_failed" # Define condição, nesse caso se nenhuma anterior falhou
    )

    notif_b_task = PythonOperator(
        task_id='notif_b', # Id da tarefa
        python_callable=notif_b, # Chama a função
        trigger_rule="one_failed" # Define condição, nesse caso só vai rodar se ao menos uma falhou
    )

    # Define dependencias
    [ download_failed_task, download_succeed_task ] >> process_task
    [ download_website_a_task, download_website_b_task ] >> download_failed_task
    [ download_website_a_task, download_website_b_task ] >> download_succeed_task
    process_task >> [ notif_a_task, notif_b_task ]