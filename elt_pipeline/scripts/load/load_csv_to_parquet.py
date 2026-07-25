import os
import json
import pyarrow as pa
import pandas as pd
import pyarrow.parquet as pq
import numpy as np

def get_latest_file_in_dir(dir, extension):
    files = [os.path.join(dir, f) for f in os.listdir(dir) if f.endswith(extension)]

    if not files:
        return None

    latest_file = max(files, key=os.path.getmtime)

    return latest_file

def load_json_from_file(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json_to_parquet(data, output_filepath):
    df = pd.DataFrame(data)
    df = df.convert_dtypes()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype('string')

    df.to_parquet(output_filepath, engine='pyarrow', index=False)

def load_db_to_dl(input_dir, output_dir):
    extension = ".json"

    latest_file = get_latest_file_in_dir(input_dir, extension)

    if latest_file:
        data = load_json_from_file(latest_file)
        print(f"Read file {latest_file}")

        fileName = os.path.basename(latest_file).replace(".json", '.parquet')
        output_filepath = os.path.join(output_dir, fileName)

        save_json_to_parquet(data, output_filepath)
        print(f"Saved Parquet file: {output_filepath}")
    else: 
        print("No JSON files found in dir")

def load_api_to_parquet():
    games_input_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\raw\games"
    games_output_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_api_games_to_parquet"
    schedule_input_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\raw\schedule"
    schedule_output_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_api_schedule_to_parquet"
    player_stat_input_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\raw\player_stats"
    player_stat_output_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_api_player_stat_to_parquet"
    team_stat_input_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\raw\team_stats"
    team_stat_output_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_api_team_stat_to_parquet"
    os.makedirs(games_output_dir, exist_ok=True)
    os.makedirs(schedule_output_dir, exist_ok=True)
    os.makedirs(player_stat_output_dir, exist_ok=True)
    os.makedirs(team_stat_output_dir, exist_ok=True)
    load_db_to_dl(games_input_dir, games_output_dir)
    load_db_to_dl(schedule_input_dir, schedule_output_dir)
    load_db_to_dl(player_stat_input_dir, player_stat_output_dir)
    load_db_to_dl(team_stat_input_dir, team_stat_output_dir)

load_api_to_parquet()
