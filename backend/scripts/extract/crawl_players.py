import pandas as pd
import json
import datetime

def crawl_players():
    # Duong dan toi file csv
    csv_path = r"D:\HocTap\DATA ENGINEERS\Project\New folder\assets\data\Players.csv"

    # Doc file csv bang dataframe
    df = pd.read_csv(csv_path)

    print("Start reading players file csv")

    # Chuyen Dataframe thanh list dictionary (JSON)
    list_players = df.to_dict(orient="records")

    # Tao duong dan file luu du lieu tho vao file json co dinh kem ngay thang
    date = datetime.date.today().strftime("%Y_%m_%d")
    path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/raw/players/crawl_players_{date}.json"

    # Chuyen List thanh dinh dang json
    json_object = json.dumps(list_players, indent=4, ensure_ascii=False)

    # Ghi JSON data vao file
    with open(path, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)
    print(f"Data saved to {path}")
    
crawl_players()