import psycopg2
import json
import os
from psycopg2.extras import execute_values

def read_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"❌ Lỗi đọc file {file_path}: {e}")
        return []

def get_id_mapping(table_name, id_column, key_column):
    query = f"SELECT {key_column}, {id_column} FROM {table_name}"

    with psycopg2.connect(
        host="localhost",
        database="nba_dw",
        user="postgres_user",
        password="postgres_password"
    ) as conn:
         with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return {row[0]: row[1] for row in rows} 

def get_latest_file_in_directory(directory, extension):
    """
    Get the latest file in a directory with a specific extension.
    
    :param directory: Directory to search for files.
    :param extension: File extension to look for.
    :return: Path to the latest file or None if no files are found.
    """
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def insert_data_from_json(data, table_name, columns, conflict_columns):
    """
    Insert data from a JSON file into a PostgreSQL table.
    
    :param file_path: Path to the JSON file.
    :param table_name: Name of the PostgreSQL table.
    :param columns: List of columns to insert data into.
    :param conflict_columns: List of columns to check for conflicts.
    """
    if not data:
        print("No data")
        return

    columns_str = ', '.join(columns)
    conflict_columns_str = ', '.join(conflict_columns)
    
    query = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES %s
        ON CONFLICT ({conflict_columns_str}) DO NOTHING
    """

    values_data = [
        tuple(record.get(key) for key in columns) for record in data
    ] 

    conn = psycopg2.connect(
        host="localhost",
        database="nba_dw",
        user="postgres_user",
        password="postgres_password"
    )
    with conn.cursor() as cur:
        execute_values(cur, query, values_data)
        print(
            f"✅ Đã insert thành công {len(values_data)} dòng vào bảng '{table_name}'!"
        )
        conn.commit()
    print(f"Inserted data into {table_name}")

def load_json_to_db_1():
    # Define directory and table information
    city_directory = r'D:\HocTap\DATA ENGINEERS\Project\New folder\backend\data\processed\transformed_to_db_city'
    city_latest_file = get_latest_file_in_directory(city_directory, ".json")

    if city_latest_file:
        print(f"📖 Đang load file: {city_latest_file}")
        # Map rõ ràng: Cột DB là 'city_name', nhưng Key trong file JSON là 'city'
        city_data = read_json_file(city_latest_file)
        insert_data_from_json(
            data=city_data,
            table_name="city",
            columns=["city"],
            conflict_columns=["city"],
        )
    else:
        print("⚠️ Không tìm thấy file JSON nào!")

    city_map = get_id_mapping(
         table_name="city", id_column="cityID", key_column="city"
    )

    league_dir = r'D:\HocTap\DATA ENGINEERS\Project\New folder\backend\data\processed\transformed_to_db_league'
    league_latest_file = get_latest_file_in_directory(league_dir, ".json")

    if league_latest_file:
        print(f"Reading file: {league_latest_file}")
        league_data = read_json_file(league_latest_file)
        insert_data_from_json(
            data=league_data,
            table_name="league",
            columns=['league'],
            conflict_columns=['league']
        )
    else: print("Can't find JSON file")

    league_map = get_id_mapping(
        table_name="league", id_column="leagueID", key_column="league"
    )

    team_dir = r'D:\HocTap\DATA ENGINEERS\Project\New folder\backend\data\processed\transformed_to_db_team'
    team_latest_file = get_latest_file_in_directory(team_dir, ".json")
    
    if team_latest_file:
        team_data = read_json_file(team_latest_file)
        
        insert_data_from_json(
            data=team_data,
            table_name="team",
            columns=['teamId'],
            conflict_columns=['teamId']
        )
    else: print("Can't find JSON file")

    team_league_dir = r'D:\HocTap\DATA ENGINEERS\Project\New folder\backend\data\processed\transformed_to_db_team_league'
    team_league_latest_file = get_latest_file_in_directory(team_league_dir, ".json")
    
    if team_league_latest_file:
            print(f"Reading file: {team_league_latest_file}")
            team_league_data = read_json_file(team_league_latest_file)

            for record in team_league_data:
                city_name = record.get("city")
                record["cityID"] = city_map.get(city_name)
                league_name = record.get("league")
                record["leagueID"] = league_map.get(league_name)
            insert_data_from_json(
                data=team_league_data,
                table_name="team_league",
                columns=['teamId','cityID', 'leagueID', 'teamName', 'teamAbbrev','seasonFounded', "seasonActiveTill"],
                conflict_columns=['teamId', 'cityID', 'seasonFounded']
            )
    else: print("Can't find JSON file")

load_json_to_db_1()