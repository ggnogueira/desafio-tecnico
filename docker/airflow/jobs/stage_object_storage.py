import os
import sys
from datetime import date
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import current_date

RAW_BUCKET = os.environ.get("RAW_BUCKET")
STG_BUCKET = os.environ.get("STG_BUCKET")

def create_spark_session(app_name: str) -> SparkSession:
    """Create and return a Spark session."""
    return SparkSession.builder.appName(app_name).getOrCreate()

def main():
    # Get command line arguments
    s3_raw_path = sys.argv[1]

    # Set up Spark session
    spark = create_spark_session("stage_database")

    # Set up Storage Paths
    s3_stg_path = f"s3a://{STG_BUCKET}/files/gcp/date={date.today()}/"

    try:
        # Read data from PostgreSQL
        df = (
            spark
            .read
            .parquet(s3_raw_path)
        )
        df.printSchema()
        df.show(truncate=False)
        # Write data to S3
        (
            df
            .write
            .mode("overwrite")
            .parquet(s3_stg_path)
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
