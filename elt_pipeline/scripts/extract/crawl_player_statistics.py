import pandas as pd
import datetime
import json
import os

def crawl_player_statistics():
    csv_path = r"D:\HocTap\DATA ENGINEERS\Project\New folder\assets\data\PlayerStatistics.csv"

    df = pd.read_csv(csv_path)

    print("Start reading player statistics file")

    list_player_stats = df.to_dict(orient="records")

    date = datetime.date.today().strftime("%Y_%m_%d")
    path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/elt_pipeline/data/raw/player_stats\crawl_player_stats_{date}.json"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    json_object = json.dumps(list_player_stats, indent=4, ensure_ascii=False)

    with open (path, "w", encoding="utf-8") as file:
        file.write(json_object)
    print (f"Data save to {path}")

crawl_player_statistics()