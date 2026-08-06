import pandas as pd
import datetime
from sqlalchemy import create_engine
import os

def read_query_from_file(file):
    with open(file, 'r', encoding="utf-8") as f:
        query = f.read()

    return query

def query_to_parquet(query, engine, parquet_file_path):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    df.to_parquet(parquet_file_path, engine="pyarrow")

def load_db_player_tb_to_parquet():
    DATABASE_TYPE = 'postgresql'
    ENDPOINT = 'postgres_dw'
    USER = 'postgres_user'
    PASSWORD = 'postgres_password'
    PORT = 5432
    DATABASE = 'nba_dw'

    engine = create_engine(f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
    query_file_path = "/opt/airflow/elt_pipeline/scripts/extract/extract_db_player_tb_to_parquet.sql"

    date = datetime.date.today().strftime("%Y_%m_%d")
    parquet_file_path = f"/opt/airflow/elt_pipeline/data/completed/load_db_to_dl/load_player_tb_to_dl/load_db_player_tb_to_dl_{date}.parquet"

    os.makedirs(os.path.dirname(parquet_file_path), exist_ok=True)

    query = read_query_from_file(query_file_path)

    query_to_parquet(
        query=query,
        engine=engine,
        parquet_file_path=parquet_file_path
    )
    print(f"Saved data from database to parquet successfully")

load_db_player_tb_to_parquet()