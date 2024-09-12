import os
import sys
from datetime import date
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import current_date


def create_spark_session(app_name: str) -> SparkSession:
    """Create and return a Spark session."""
    return SparkSession.builder.appName(app_name).getOrCreate()

def read_from_postgres(spark: SparkSession, jdbc_url: str, table: str, properties: dict) -> DataFrame:
    """Read data from PostgreSQL using Spark JDBC."""
    return (
        spark
        .read
        .jdbc(url=jdbc_url, table=table, properties=properties)
    )

def write_to_s3(df: DataFrame, bucket: str, database: str, schema: str, table: str) -> None:
    """Write DataFrame to S3 as Parquet."""
    s3_path = f"s3a://{bucket}/postgres/{database}/{schema}/{table}/date={date.today()}"
    (
        df
        .write
        .mode("overwrite")
        .parquet(s3_path)
    )

def main():
    # Get command line arguments
    #base_url = f"jdbc:postgresql://{host}:{port}/{database}"
    base_url = f"jdbc:postgresql://34.173.103.16:5432/postgres"

    #jdbc_url = sys.argv[1]
    table = sys.argv[1]

    # Set up Spark session
    spark = create_spark_session("raw_database")

    # Set up JDBC connection properties
    properties = {
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "driver": "org.postgresql.Driver"
    }

    try:
        # Read data from PostgreSQL
        df = read_from_postgres(spark, base_url, table, properties)

        # Write data to S3
        write_to_s3(
            df,
            bucket=os.environ["RAW_BUCKET"],
            database=os.environ["DB_NAME"],
            schema=os.environ["DB_SCHEMA"],
            table=table
        )

        print(f"Successfully extracted and stored data for table: {table}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
