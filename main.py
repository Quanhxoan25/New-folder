import pandas as pd

parquet_part = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_api_games_to_parquet\crawl_games_2026_07_23.parquet"

df = pd.read_parquet(parquet_part)

print(df.head)