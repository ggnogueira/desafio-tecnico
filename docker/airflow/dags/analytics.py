from datetime import datetime, timedelta
from airflow.decorators import dag, task
from custom_operators.Lambda import lambda_operator
from custom_operators.Spark import spark_submit_operator
import json


@dag(
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['data lake'],
)
def analytics_dag():
    """
    Database Load DAG
    """
    @task()
    def consolidate():
        """
        Extract data from Postgres Database
        """
        spark_submit_operator('analytics').execute(context=None)
        return True

    @task()
    def load():
        """
        Load data to Postgres
        """
        spark_submit_operator('load').execute(context=None)
        return True

    consolidate() >> load()

curated_dag = analytics_dag()
