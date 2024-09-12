from datetime import datetime, timedelta
from airflow.decorators import dag, task
from custom_operators.Lambda import lambda_operator
from custom_operators.Spark import spark_submit_operator
import json


@dag(
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['postgres'],
)
def database_dag():
    """
    Database Load DAG
    """
    @task(pool='lambda')
    def extract():
        """
        Extract data from Postgres Database
        """
        spark_submit_operator('raw_database', args=['venda']).execute(context=None)
        return True

    @task()
    def transform(lambda_response):
        """
        Transform data from Postgres
        """
        spark_submit_operator('stage_database', args=['postgres', 'public', 'venda']).execute(context=None)
        return True

    @task()
    def load(some_data):
        """
        Load data from Postgres
        """
        pass

    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)

database_dag = database_dag()
