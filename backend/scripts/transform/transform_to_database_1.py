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
    return df.replace(r'^\s*$', np.nan, regex=True).drop_duplicates().dropna()

def save_to_json(df, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        df.to_json(
            f,
            orient="records",
            indent=4,
            force_ascii=False, 
        )
    print(f"Save dataframe to {filename}")

def transform_to_db1():
    file_path = r"D:\HocTap\DATA ENGINEERS\Project\New folder\backend\data\raw\teams"
    raw_teams  = read_latest_file_in_dir(file_path)

    date = datetime.date.today().strftime("%Y_%m_%d")

    team_league = []
    league = []
    city = []
    team_list = []
    for team in raw_teams:
        team_league.append(
            {
                "teamId": team.get("teamId"),
                "league": team.get("league"),
                "teamName": team.get("teamName"),
                "teamAbbrev": team.get("teamAbbrev"),
                "city": team.get("teamCity"),
                "seasonFounded": team.get("seasonFounded"),
                "seasonActiveTill": team.get("seasonActiveTill"),
            }
        )       
        team_list.append(
            {
                "teamId": team.get("teamId"),
            }
        ) 
        league.append(
            {
                'league': team.get('league')
            }
        )
        city.append(
            {
                'city': team.get('teamCity')
            }
        )
    team_list_df = cleaned_dataframe(pd.DataFrame(team_list))
    team_league_df = cleaned_dataframe(pd.DataFrame(team_league))
    league_df = cleaned_dataframe(pd.DataFrame(league))
    city_df = cleaned_dataframe(pd.DataFrame(city))
    
    dir_path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/processed"

    os.makedirs(os.path.dirname(dir_path), exist_ok=True)

    team_path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/processed/transformed_to_db_team/process_team_{date}.json"
    team_league_path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/processed/transformed_to_db_team_league/process_team_league_{date}.json"
    league_path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/processed/transformed_to_db_league/process_league_{date}.json"
    city_path = f"D:/HocTap/DATA ENGINEERS/Project/New folder/backend/data/processed/transformed_to_db_city/process_city_{date}.json"
    save_to_json(team_list_df, team_path)
    save_to_json(team_league_df, team_league_path)
    save_to_json(league_df, league_path)
    save_to_json(city_df, city_path)

    

transform_to_db1()