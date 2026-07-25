import os
import json
import numpy as np
import datetime
import pandas as pd

def get_latest_file (directory, extension):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]

    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def read_latest_file_in_dir(directory):
    extension = ".json"
    latest_file = get_latest_file(directory, extension)
    if latest_file:
        with open(latest_file, "r", encoding="utf-8") as file:
            data_json = json.load(file)
        print(f"Transforming from file: {latest_file}")
    else:
        print("No file found")
        data_json = []
    return data_json

def cleaned_dataframe(df):
    nullable_columns = ["toYear"]

    # Các cột còn lại là bắt buộc
    required_columns = [col for col in df.columns if col not in nullable_columns]
    #loai bo chuoi rong hoac chi chua khoangg trang, xoa cac dong bi trung lap, dropna xoa cac dong chua NaN
    return df.replace(r'^\s*$', np.nan, regex=True).drop_duplicates().dropna(subset=required_columns)

def save_to_json(df, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        df.to_json(
            f,
            orient="records",
            indent=4,
            force_ascii=False,  # Giữ nguyên ký tự đặc biệt (é, á, ñ...)
        )
    print(f"Save dataframe to {filename}")

def transform_to_db2():
    file_path = r"D:\HocTap\DATA ENGINEERS\Project\New folder\backend\data\raw\players"
    raw_players  = read_latest_file_in_dir(file_path)

    date = datetime.date.today().strftime("%Y_%m_%d")

    countries = []
    schools = []
    player_list = []

    for player in raw_players:
        countries.append({
            "country": player.get("country")
        })
        schools.append({
            "school": player.get("school")
        })
        player_list.append({
            "personID": player.get("personId"),
            "firstName": player.get("firstName"),
            "lastName": player.get("lastName"),
            "birthDate": player.get("birthDate"),
            "school": player.get("school"),
            "country": player.get("country"),
            "draftYear": player.get("draftYear"),
            "draftRound": player.get("draftRound"),
            "draftNumber": player.get("draftNumber"),
            "heightInches": player.get("heightInches"),
            'bodyWeightLbs': player.get('bodyWeightLbs'),
            "jersey": player.get('jersey'),
            'guard': player.get('guard'),
            'forward': player.get('forward'),
            'center': player.get('center'),
            "dleagueFlag": player.get('dleagueFlag'),
            "nbaFlag": player.get('nbaFlag'),
            "gamesPlayedFlag": player.get('gamesPlayedFlag'),
            "fromYear": player.get('fromYear'),
            "toYear": player.get('toYear')
        })

    country_df = cleaned_dataframe(pd.DataFrame(countries))
    school_df = cleaned_dataframe(pd.DataFrame(schools))
    player_df = cleaned_dataframe(pd.DataFrame(player_list))

    dir_path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/processed"

    os.makedirs(os.path.dirname(dir_path), exist_ok=True)

    country_path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/processed/transformed_to_db_counry/process_country_{date}.json"
    schools_path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/processed/transformed_to_db_school/process_school_{date}.json"
    players_path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/processed/transformed_to_db_player/process_player_{date}.json"
    save_to_json(country_df, country_path)
    save_to_json(school_df, schools_path)
    save_to_json(player_df, players_path)

    

transform_to_db2()