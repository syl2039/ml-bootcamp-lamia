# Importações necessárias
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator

# Função responsável por criar as subdags
def factory_subdag(parent_dag_name, child_dag_name, default_args):

    with DAG(
        dag_id='%s.%s' % (parent_dag_name, child_dag_name),
        default_args=default_args
    ) as dag:
        for i in range(5):
            DummyOperator(
                task_id='%s-task-%s' % (child_dag_name, i + 1)
            )

    return dag