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
def object_storage_dag():
    """
    Object Storage Load DAG
    """
    @task(pool='lambda')
    def extract():
        """
        Extract data from Object Storage
        """
        response = lambda_operator('crawler-object-storage')
        print(response)
        return response

    @task()
    def transform(lambda_response):
        """
        Transform data from Object Storage
        """
        print(lambda_response)
        file_path = lambda_response.get('body')
        spark_submit_operator('stage_object_storage', args=[file_path]).execute(context=None)
        return True

    @task()
    def load(some_data):
        """
        Load data from Object Storage
        """
        pass

    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)

object_storage_dag = object_storage_dag()
