import pandas as pd
import datetime
import json
import os

def crawl_games():
    csv_path = "/opt/airflow/assets/data/Games.csv"

    df = pd.read_csv(csv_path)

    print("Starting reading games file")

    list_players = df.to_dict(orient="records")

    date = datetime.date.today().strftime("%Y_%m_%d")
    
    path = f"/opt/airflow/elt_pipeline/data/raw/games/crawl_games_{date}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    json_object = json.dumps(list_players, indent=4, ensure_ascii=False)

    with open (path, "w", encoding="utf-8") as file:
        file.write(json_object)
    print (f"Data save to {path}")

crawl_games()
