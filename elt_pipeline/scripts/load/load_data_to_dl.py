from minio import Minio
import os
from concurrent.futures import ThreadPoolExecutor

def get_latest_file (directory, extension):
    if not os.path.exists(directory):
        return None
    
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]

    if not files:
        return None
    last_file= max(files, key=os.path.getmtime)
    return last_file

def upload_single_file(file_info, client, bucket_name):
    local_part, minio_part = file_info
    client.fput_object(bucket_name, minio_part, local_part)
    print(f"Upload successfully: {minio_part}")

def load_data_to_dl():
    extension = ".parquet"

    games_parquet_dir_part = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_api_games_to_parquet"
    player_stats_parquet_dir_part = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_api_player_stat_to_parquet"
    schedule_parquet_dir_part = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_api_schedule_to_parquet"
    team_stats_parquet_dir_part = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_api_team_stat_to_parquet"
    player_parquet_dir_part = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_db_to_dl\load_player_tb_to_dl"
    team_parquet_dir_part = r"D:\HocTap\DATA ENGINEERS\Project\New folder\elt_pipeline\data\completed\load_db_to_dl\load_team_tb_to_dl"

    games_latest_file = get_latest_file(games_parquet_dir_part, extension)
    player_stats_latest_file = get_latest_file(player_stats_parquet_dir_part, extension)
    team_stats_latest_file = get_latest_file(team_stats_parquet_dir_part, extension)
    schedule_latest_file = get_latest_file(schedule_parquet_dir_part, extension)
    player_latest_file = get_latest_file(player_parquet_dir_part, extension)
    team_latest_file = get_latest_file(team_parquet_dir_part, extension)

    games_minio_part = f"raw/api/games/{os.path.basename(games_latest_file)}"
    player_stats_minio_part = f"raw/api/player_stats/{os.path.basename(player_stats_latest_file)}"
    team_stats_minio_part = f"raw/api/team_stats/{os.path.basename(team_stats_latest_file)}"
    schedule_minio_part = f"raw/api/schedules/{os.path.basename(schedule_latest_file)}"
    player_minio_part = f"raw/db/players/{os.path.basename(player_latest_file)}"
    team_minio_part = f"raw/db/teams/{os.path.basename(team_latest_file)}"

    file_info = [
        (games_latest_file, games_minio_part),
        (player_stats_latest_file, player_stats_minio_part),
        (schedule_latest_file, schedule_minio_part),
        (team_stats_latest_file,team_stats_minio_part),
        (player_latest_file, player_minio_part),
        (team_latest_file, team_minio_part)
    ]


    client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadminpassword",
        secure=False
    )

    bucket_name = "basketball-data"
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(upload_single_file, item, client, bucket_name)
            for item in file_info
        ]

        for future in futures:
            future.result()

load_data_to_dl()