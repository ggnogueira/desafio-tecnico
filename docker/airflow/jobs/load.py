import os
import sys
from datetime import date
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import current_date

ANALYTICS_BUCKET = os.environ["ANALYTICS_BUCKET"]

def create_spark_session(app_name: str) -> SparkSession:
    """Create and return a Spark session."""
    return SparkSession.builder.appName(app_name).getOrCreate()

def read_from_path(spark: SparkSession, path: str) -> DataFrame:
    """Read data from Minio using Spark."""
    return (
        spark
        .read
        .parquet(path)
    )

def main():

    # Set up Spark session
    spark = create_spark_session("analytics")

    # Set up paths
    path_fato_vendas = f"s3a://{ANALYTICS_BUCKET}/fato_venda/"
    path_dim_categorias = f"s3a://{ANALYTICS_BUCKET}/dim_categoria/"
    path_dim_usuarios = f"s3a://{ANALYTICS_BUCKET}/dim_usuario/"
    path_dim_data = f"s3a://{ANALYTICS_BUCKET}/dim_data/"

    path_total_vendas_por_usuario = f"s3a://{ANALYTICS_BUCKET}/total_vendas_por_usuario/"
    path_quantidade_vendas_por_categoria = f"s3a://{ANALYTICS_BUCKET}/quantidade_vendas_por_categoria/"
    path_media_vendas_por_categoria = f"s3a://{ANALYTICS_BUCKET}/media_vendas_por_categoria/"

    # Set up JDBC connection properties
    properties = {
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "driver": "org.postgresql.Driver"
    }
    base_url = f"jdbc:postgresql://postgres-local:5432/db"

    try:
        df_fato_vendas = read_from_path(spark, path_fato_vendas)
        print("Fato - Venda")
        df_fato_vendas.show()
        print(df_fato_vendas.count())
        (
            df_fato_vendas
            .write
            .jdbc(url=base_url, table="fato_vendas", mode="overwrite", properties=properties)
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

    try:
        df_dim_categorias = read_from_path(spark, path_dim_categorias)
        print("Dimensao - Categoria")
        df_dim_categorias.show()
        (
            df_dim_categorias
            .write
            .jdbc(url=base_url, table="dim_categorias", mode="overwrite", properties=properties)
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

    try:
        df_dim_usuarios = read_from_path(spark, path_dim_usuarios)
        print("Dimensao - Usuario")
        df_dim_usuarios.show()
        (
            df_dim_usuarios
            .write
            .jdbc(url=base_url, table="dim_usuarios", mode="overwrite", properties=properties)
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

    try:
        df_dim_data = read_from_path(spark, path_dim_data)
        print("Dimensao - Data")
        df_dim_data.show()
        (
            df_dim_data
            .write
            .jdbc(url=base_url, table="dim_data", mode="overwrite", properties=properties)
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

    try:
        df_quantidade_vendas_por_categoria = read_from_path(spark, path_quantidade_vendas_por_categoria)
        (
            df_quantidade_vendas_por_categoria
            .write
            .jdbc(url=base_url, table="quantidade_vendas_por_categoria", mode="overwrite", properties=properties)
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

    try:
        df_total_vendas_por_usuario = read_from_path(spark, path_total_vendas_por_usuario)
        (
            df_total_vendas_por_usuario
            .write
            .jdbc(url=base_url, table="total_vendas_por_usuario", mode="overwrite", properties=properties)
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

    try:
        df_media_vendas_por_categoria = read_from_path(spark, path_media_vendas_por_categoria)
        (
            df_media_vendas_por_categoria
            .write
            .jdbc(url=base_url, table="media_vendas_por_categoria", mode="overwrite", properties=properties)
        )
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

    print(f"Successfully created dim, facts and consolidated data")

if __name__ == "__main__":
    main()
