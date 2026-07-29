import duckdb
import os

database_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
sql_file = r'D:\HocTap\DATA ENGINEERS\Project\New folder\sql\config_dw\dw_config.sql'
os.makedirs(os.path.dirname(database_path), exist_ok=True)

if os.path.exists(database_path):
    os.remove(database_path)

conn = duckdb.connect(database=database_path)

with open(sql_file, 'r') as file:
    sql_script = file.read()

conn.execute(sql_script)

conn.execute(sql_script)

conn.close()

print(f"Create database successfully in {database_path}")