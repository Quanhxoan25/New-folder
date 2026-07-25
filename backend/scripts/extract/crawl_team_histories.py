import pandas as pd
import json
import datetime

def crawl_team_histories():
    # Duong dan toi file csv
    csv_path = r"D:\HocTap\DATA ENGINEERS\Project\New folder\assets\data\TeamHistories.csv"

    # Doc file csv bang dataframe
    df = pd.read_csv(csv_path)

    print("Start reading teams file csv")

    # Chuyen Dataframe thanh list dictionary (JSON)
    list_teams = df.to_dict(orient="records")

    # Tao duong dan file luu du lieu tho vao file json co dinh kem ngay thang
    date = datetime.date.today().strftime("%Y_%m_%d")
    path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/raw/teams/crawl_teams_{date}.json"

    # Chuyen List thanh dinh dang json
    json_object = json.dumps(list_teams, indent=4, ensure_ascii=False)

    # Ghi JSON data vao file
    with open(path, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)
    print(f"Data saved to {path}")

crawl_team_histories()
