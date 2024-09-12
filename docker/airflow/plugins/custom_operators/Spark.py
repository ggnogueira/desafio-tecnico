from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import os

def spark_submit_operator(job_name, args=None):
    spark_conf = {
        'spark.driver.extraJavaOptions': '-Divy.cache.dir=/tmp -Divy.home=/tmp -Dcom.amazonaws.sdk.disableCertChecking=true',
        'spark.hadoop.fs.s3a.endpoint': os.environ["AWS_ENDPOINT_URL"],
        'spark.hadoop.fs.s3a.access.key': os.environ["AWS_ACCESS_KEY_ID"],
        'spark.hadoop.fs.s3a.secret.key': os.environ["AWS_SECRET_ACCESS_KEY"],
        'spark.hadoop.fs.s3a.path.style.access': 'true',
        'spark.hadoop.fs.s3a.impl': 'org.apache.hadoop.fs.s3a.S3AFileSystem',
        'spark.hadoop.fs.s3a.aws.credentials.provider': 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider'
    }

    return SparkSubmitOperator(
        task_id='spark_task',
        application=f'/opt/airflow/jobs/{job_name}.py',
        application_args=args or [],
        conn_id='spark_default',
        executor_cores='4',
        executor_memory='2g',
        num_executors='1',
        name='airflow-spark-job',
        verbose=True,
        conf=spark_conf,
        packages='org.apache.hadoop:hadoop-aws:3.3.4,org.postgresql:postgresql:42.2.18'
    )
