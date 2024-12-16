# Importações necessárias
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
from airflow.operators.bash_operator import BashOperator
import numpy as np
import pandas as pd
from random import randint, sample
import datetime
import time
import calendar

args = { # Argumentos 
    'owner': 'Airflow', # Nome do dono
    'start_date': airflow.utils.dates.days_ago(1), # Data de início (1 dia atrás)
}

# Função que gera datas aleatórias
def generate_random_dates(start, end, n):
    dates = pd.Series(np.zeros(n)) # Cria um vetor de tamanho n zerados
    for i in range(n):
        dates[i] = start + datetime.timedelta(seconds=randint(0, int((end - start).total_seconds()))) # Gera uma data aleatória
    return(dates) # Retorna o vetor coms as datas

# Função que gera pedidos aleatórios
def push_xcom_with_return():
    n = 1000000 # Número de linhas
    # cria um dataframe com dados aleatórios
    df = pd.DataFrame({'user_id': sample(range(90000000, 99999999), n),
                    'order_id': np.random.choice(range(1000000, 2000000), n, replace=False),
                    'order_date': generate_random_dates(datetime.date(2015, 1, 1), 
                                                        datetime.date(2017, 12, 31), 
                                                        n),
                    'number_of_products': np.random.choice(range(20), n, replace=True),
                    'total_amount': np.round(np.random.uniform(1, 5000, n), 2)})

    # adiciona uma nova coluna com o dia da semana correspondente a data
    df = df.assign(day_of_week = df.order_date.apply(lambda x: calendar.day_name[x.weekday()]))
    
    df.user_id = df.user_id.astype('str') # Troca para string
    df.order_id = df.order_id.astype('str') # Troca para string

    return df

# Função que recebe o contexto da tarefa e printa
def get_pushed_xcom_with_return(**context):
    print(context['ti'].xcom_pull(task_ids='t0')) 

# Cria uma dag que vai ser executada somente uma vez
with DAG(dag_id='xcom_dag_big', default_args=args, schedule_interval="@once") as dag:
    
    t0 = PythonOperator(
        task_id='t0', # id da tarefa
        python_callable=push_xcom_with_return # Chama a função
    )

    t1 = PythonOperator(
        task_id='t1', # id da tarefa
        provide_context=True, # da o contexto
        python_callable=get_pushed_xcom_with_return # Chama a função
    )
    # Fluxo de Execução
    t0 >> t1