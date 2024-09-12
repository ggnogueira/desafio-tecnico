import os
import sys
from datetime import date
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import current_date

STG_BUCKET = os.environ["STG_BUCKET"]
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

def write_to_s3(df: DataFrame, bucket: str, dataset: str) -> None:
    """Write DataFrame to S3 as Parquet."""
    s3_path = f"s3a://{bucket}/{dataset}/"
    (
        df
        .write
        .mode("overwrite")
        .parquet(s3_path)
    )

def main():

    # Set up Spark session
    spark = create_spark_session("analytics")

    # Set up paths
    path_vendas = f"s3a://{STG_BUCKET}/postgres/postgres/public/venda/date={date.today()}/"
    path_categorias = f"s3a://{STG_BUCKET}/files/gcp/date={date.today()}/"
    path_usuarios = f"s3a://{STG_BUCKET}/api/date={date.today()}/"

    try:
        # Read Vendas data
        df_vendas = read_from_path(spark, path_vendas)
        df_vendas.createOrReplaceTempView("tb_venda")
        df_fato_venda = spark.sql("""
        SELECT
            id_venda,
            CAST(REPLACE(data_venda, '-', '') AS INT) AS id_data,
            id_funcionario as id_usuario,
            id_categoria,
            venda AS valor_venda,
            1 AS quantidade
        FROM tb_venda;
        """)

        # Read Usuarios data
        df_usuarios = read_from_path(spark, path_usuarios)
        df_usuarios.createOrReplaceTempView("tb_usuario")
        df_dim_usuarios = spark.sql("""
        SELECT
            id as id_usuario,
            nome
        FROM tb_usuario;
        """)

        # Read Categorias data
        df_categorias = read_from_path(spark, path_categorias)
        df_categorias.createOrReplaceTempView("tb_categoria")
        df_dim_categorias = spark.sql("""
        SELECT
            id as id_categoria,
            nome_categoria
        FROM tb_categoria;
        """)

        df_dim_data = spark.sql("""
        SELECT DISTINCT
            CAST(REPLACE(data_venda, '-', '') AS INT) AS id_data,
            data_venda AS data,
            EXTRACT(DAY FROM data_venda) AS dia,
            EXTRACT(MONTH FROM data_venda) AS mes,
            EXTRACT(YEAR FROM data_venda) AS ano,
            EXTRACT(QUARTER FROM data_venda) AS trimestre
        FROM tb_venda;
        """)

        df_total_vendas_por_usuario = spark.sql("""
        SELECT
            u.id, u.nome, COALESCE(SUM(v.venda), 0) AS total_vendas
        FROM tb_usuario u
        LEFT JOIN tb_venda v ON u.id = v.id_funcionario
        GROUP BY u.id, u.nome;
        """)

        df_quantidade_vendas_por_categoria = spark.sql("""
        SELECT
            c.id, c.nome_categoria, COUNT(v.id_venda) AS quantidade_vendas
        FROM tb_categoria c
        LEFT JOIN tb_venda v ON c.id = v.id_categoria
        GROUP BY c.id, c.nome_categoria;
        """)

        df_media_vendas_por_categoria = spark.sql("""
        SELECT
            c.id, c.nome_categoria, AVG(v.venda) AS media_vendas
        FROM tb_categoria c
        LEFT JOIN tb_venda v ON c.id = v.id_categoria
        GROUP BY c.id, c.nome_categoria;
        """)

        # Write data to S3
        write_to_s3(
            df_fato_venda,
            bucket=ANALYTICS_BUCKET,
            dataset="fato_venda",
        )
        write_to_s3(
            df_dim_categorias,
            bucket=ANALYTICS_BUCKET,
            dataset="dim_categoria",
        )
        write_to_s3(
            df_dim_usuarios,
            bucket=ANALYTICS_BUCKET,
            dataset="dim_usuario",
        )
        write_to_s3(
            df_dim_data,
            bucket=ANALYTICS_BUCKET,
            dataset="dim_data",
        )
        write_to_s3(
            df_total_vendas_por_usuario,
            bucket=ANALYTICS_BUCKET,
            dataset="total_vendas_por_usuario",
        )
        write_to_s3(
            df_quantidade_vendas_por_categoria,
            bucket=ANALYTICS_BUCKET,
            dataset="quantidade_vendas_por_categoria",
        )
        write_to_s3(
            df_media_vendas_por_categoria,
            bucket=ANALYTICS_BUCKET,
            dataset="media_vendas_por_categoria",
        )
        print(f"Successfully created dim, facts and consolidated data")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
