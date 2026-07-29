import duckdb

duckdb_part = r"D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb"
conn = duckdb.connect(duckdb_part)

conn.execute('LOAD httpfs')

conn.execute("""
    CREATE OR REPLACE SECRET minio_secret (
        TYPE s3,
        PROVIDER config,
        KEY_ID 'minioadmin',
        SECRET 'minioadminpassword',
        ENDPOINT 'localhost:9000',
        REGION 'us-east-1',
        URL_STYLE 'path',
        USE_SSL false
    )
""")

games_path = "s3://basketball-data/raw/api/games/*.parquet"

total_games = conn.execute(
    f"SELECT COUNT(*) FROM read_parquet('{games_path}')"
).fetchone()[0]

print(f"Connected to MinIO successfully. Total games: {total_games}")

conn.close()