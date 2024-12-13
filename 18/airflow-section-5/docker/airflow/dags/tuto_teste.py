# Importações necessárias
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Informações gerais
# - Criei duas novas tarefas
# - Removi as dependencias

# Resultados
# Todas as tarefas foram executadas com sucesso

default_args = { # Argumentos padrões
    "owner": "airflow", # Nome do dono
    "depends_on_past": False, # Define se a execução atual depende da anterior
    "start_date": datetime(2015, 6, 1), # Data de início
    "email": ["airflow@airflow.com"], # Email do dono
    "email_on_failure": False, # Notifica quando acontece alguma falha
    "email_on_retry": False, # Notifica quando alguma falha é tentada novamente
    "retries": 1, # Número de retentativas
    "retry_delay": timedelta(minutes=5), # Tempo de pausa pra retentativa
}

# Criação de uma DAG chamada tutorial que será executada uma vez por dia
dag = DAG("tutorial", default_args=default_args, schedule_interval=timedelta(1))

# Tarefa que printa a data
t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

# Tarefa que pausa a execução por 5 segundos, caso falhe, ela tem mais três tentativas
t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

# Comando para a tarefa 3, consiste em um for que printa a data de execução,
# a data de execução somada com 7 dias e o parametro passado
templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""
# Tarefa que chama o comando acima e passa um parametro pra ser printado
t3 = BashOperator(
    task_id="templated",
    bash_command=templated_command,
    params={"my_param": "Parameter I passed in"},
    dag=dag,
)
# Comando para a tarefa t4 que printa teste
comando_t4 = "echo 'teste'"
# Tarefa que chama o comando acima
t4 = BashOperator(task_id="print", bash_command=comando_t4, dag=dag)

# Comando para a tarefa t5 que printa a versão do python
comando_t5 = "python --version"
# Tarefa que chama o comando acima
t5 = BashOperator(task_id="print_version", bash_command=comando_t5, dag=dag)


# t2.set_upstream(t1) # Define uma dependencia
# t3.set_upstream(t1) # Define uma dependencia
