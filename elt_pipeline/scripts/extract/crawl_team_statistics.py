import pandas as pd
import datetime
import json
import os

def crawl_team_statistics():
    csv_path = "/opt/airflow/assets/data/TeamStatistics.csv"

    df = pd.read_csv(csv_path)

    print("Start reading team statistics file")

    list_team_stats = df.to_dict(orient="records")

    date = datetime.date.today().strftime("%Y_%m_%d")
    path = f"/opt/airflow/elt_pipeline/data/raw/team_stats/crawl_team_stats_{date}.json"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    json_object = json.dumps(list_team_stats, indent=4, ensure_ascii=False)

    with open (path, "w", encoding="utf-8") as file:
        file.write(json_object)
    print (f"Data save to {path}")

crawl_team_statistics()