import os
import json
import psycopg2
from psycopg2.extras import execute_values

def read_json_file(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Can't read file {file}: {e}")

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

def get_latest_file_in_dir(dir, extension):
    files = [os.path.join(dir, f) for f in os.listdir(dir) if f.endswith(extension)]
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def insert_data_from_json(data, table_name, columns, conflict_columns):
    if not data:
        print("No data read in file")
        return

    columns_str = ', '.join(columns)
    conflict_column_str = ', '.join(conflict_columns)

    query = f"""
    INSERT INTO {table_name} ({columns_str})
    VALUES %s
    ON CONFLICT ({conflict_column_str}) DO NOTHING
    """

    values_data = [
        tuple(record.get(key) for key in columns) for record in data
    ]

    with psycopg2.connect(
        host="localhost",
        database="nba_dw",
        user="postgres_user",
        password="postgres_password"
    ) as conn:
        with conn.cursor() as cur: 
            execute_values(cur, query, values_data)
            print(
                f"Successfull insert data {len(values_data)} into table {table_name}"
            )
            conn.commit()
        print(f"Inserted data into {table_name}")

def load_json_to_db2():
    country_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\backend\data\processed\transformed_to_db_counry"
    school_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\backend\data\processed\transformed_to_db_school"
    player_dir = r"D:\HocTap\DATA ENGINEERS\Project\New folder\backend\data\processed\transformed_to_db_player"
    country_latest_file = get_latest_file_in_dir(country_dir, ".json")
    school_latest_file = get_latest_file_in_dir(school_dir, ".json")
    player_latest_file = get_latest_file_in_dir(player_dir, ".json")

    if country_latest_file:
        print(f"Loading file: {country_latest_file}")

        country_data = read_json_file(country_latest_file)
        insert_data_from_json(
            data=country_data,
            table_name="country",
            columns=['country'],
            conflict_columns=['country']
        )
    else: 
        print("Cant find country file")

    if school_latest_file:
        print(f"Loading file: {school_latest_file}")

        school_data = read_json_file(school_latest_file)
        insert_data_from_json(
            data=school_data,
            table_name="school",
            columns=['school'],
            conflict_columns=['school']
        )
    else: 
        print("Cant find school file")

    country_map = get_id_mapping(
        table_name="country",
        id_column="countryID",
        key_column="country"
    )

    school_map = get_id_mapping(
        table_name="school",
        id_column="schoolID",
        key_column="school"
    )

    if player_latest_file:
        print(f"Loading file: {player_latest_file}")

        player_data = read_json_file(player_latest_file)

        for record in player_data:
            country_name = record.get("country")
            record["countryID"] = country_map.get(country_name)
            school_name = record.get("school")
            record["schoolID"] = school_map.get(school_name)
            
        insert_data_from_json(
            data=player_data,
            table_name="players",
            columns=[
                "personID",
                "firstName",
                "lastName",
                "birthDate",
                "schoolID",
                "countryID",
                "draftYear",
                "draftRound",
                "draftNumber",
                "heightInches",
                'bodyWeightLbs',
                "jersey",
                'guard',
                'forward',
                'center',
                "dleagueFlag",
                "nbaFlag",
                "gamesPlayedFlag",
                "fromYear",
                "toYear"
            ],
            conflict_columns=['firstName', 'lastName', 'birthDate']
        )
    else: 
        print("Cant find country file")

load_json_to_db2()
