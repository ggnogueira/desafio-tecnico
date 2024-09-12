from datetime import datetime, timedelta
from airflow.decorators import dag, task
from custom_operators.Lambda import lambda_operator
from custom_operators.Spark import spark_submit_operator
import json


@dag(
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['api'],
)
def api_dag():
    """
    API Load DAG
    """
    @task(pool='lambda')
    def extract():
        """
        Extract data from API
        """
        response = lambda_operator('crawler-api')
        print(response)
        return response

    @task()
    def transform(lambda_response):
        """
        Transform data from API
        """
        print(lambda_response)
        file_path = lambda_response.get('body')
        spark_submit_operator('stage_api', args=[file_path]).execute(context=None)
        return True

    @task()
    def load(some_data):
        """
        Load data from API
        """
        pass

    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)

api_dag = api_dag()
