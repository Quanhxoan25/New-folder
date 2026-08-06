import pandas as pd
import datetime
import json
import os

def crawl_schedule ():
    csv_path = "/opt/airflow/assets/data/schedules_unifield.csv"
    df = pd.read_csv(csv_path)

    print("Start reading schedule file")

    list_schedule = df.to_dict(orient="records")
    
    date = datetime.date.today().strftime("%Y_%m_%d")
    path = f"/opt/airflow/elt_pipeline/data/raw/schedule/crawl_schedule_{date}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    json_object = json.dumps(list_schedule, indent=4, ensure_ascii=False)

    with open(path, "w", encoding="utf-8") as file:
        file.write(json_object)
    print(f"Data save to {path}")

crawl_schedule()
