import duckdb

def insert_into_dim_country():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_country (
            country_id INTEGER PRIMARY KEY,
            country VARCHAR(100)
        );
    """)

    conn.execute(f"""
        INSERT INTO dim_country 
        SELECT DISTINCT country_id, country 
        FROM stg_players
        WHERE country_id IS NOT NULL
            AND country IS NOT NULL
        ON CONFLICT (country_id) DO UPDATE SET country = EXCLUDED.country
    """)

    count = conn.execute("SELECT COUNT(*) FROM dim_country").fetchone()[0]
    print(f"Tổng số quốc gia trong dim_country: {count}")

    data_table = conn.execute("SELECT * FROM dim_country").fetchall()

    print(data_table)
    conn.close()

def insert_into_dim_school():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_school (
            school_id INTEGER PRIMARY KEY,
            school VARCHAR(100)
        );
    """)

    conn.execute("""
        INSERT INTO dim_school
        SELECT DISTINCT school_id, school 
        FROM stg_players 
        WHERE school_id IS NOT NULL AND school IS NOT NULL
        ON CONFLICT(school_id) DO UPDATE SET school = EXCLUDED.school
    """)

    count = conn.execute("SELECT COUNT(*) FROM dim_school").fetchone()[0]
    print(f"Tổng số truong trong dim_school: {count}")

    data_table = conn.execute("SELECT * FROM dim_school").fetchall()

    print(data_table)
    conn.close()

def insert_into_dim_city():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("""   
        CREATE TABLE IF NOT EXISTS dim_city (
            city_id INTEGER PRIMARY KEY,
            city VARCHAR(100)
        );
    """)

    conn.execute("""
        INSERT INTO dim_city
        SELECT DISTINCT city_id, city
        FROM stg_teams
        WHERE city_id IS NOT NULL AND city IS NOT NULL
        ON CONFLICT(city_id) DO UPDATE SET city = EXCLUDED.city
    """)

    count = conn.execute("SELECT COUNT(*) FROM dim_city").fetchone()[0]
    print(f"Tổng số thanh pho trong dim_city: {count}")

    data_table = conn.execute("SELECT * FROM dim_city").fetchall()

    print(data_table)
    conn.close()

def insert_into_dim_league():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_league (
            league_id INTEGER PRIMARY KEY,
            league VARCHAR(100)
        );
    """)

    conn.execute("""
        INSERT INTO dim_league
        SELECT DISTINCT league_id, league 
        FROM stg_teams
        WHERE league_id IS NOT NULL
            AND league IS NOT NULL
        ON CONFLICT(league_id) DO UPDATE SET league = EXCLUDED.league
    """)

    count = conn.execute("SELECT COUNT(*) FROM dim_league").fetchone()[0]
    print(f"Tổng số thanh pho trong dim_league: {count}")

    data_table = conn.execute("SELECT * FROM dim_league").fetchall()

    print(data_table)
    conn.close()

def insert_into_dim_date():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id INTEGER PRIMARY KEY, 
            game_day VARCHAR(10),
            season VARCHAR(20)
        );
    """)

    conn.execute("""
        INSERT INTO dim_date
        SELECT DISTINCT 
            CAST(strftime(game_date_time_est, '%Y%m%d') AS INT) AS date_id,
            game_day, season
        FROM stag_schedules
        WHERE game_day IS NOT NULL
            AND season IS NOT NULL
        ON CONFLICT(date_id) DO UPDATE SET game_day = EXCLUDED.game_day
    """)

    count = conn.execute("SELECT COUNT(*) FROM dim_date").fetchone()[0]
    print(f"Tổng số thanh pho trong dim_date: {count}")

    data_table = conn.execute("SELECT * FROM dim_date").fetchall()

    print(data_table)
    conn.close()

def insert_into_dim_arena():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        DROP TABLE IF EXISTS dim_arena
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_arena (
            arena_id INTEGER PRIMARY KEY, 
            arena_city VARCHAR(50),
            arena_state VARCHAR(50),
            arena_name VARCHAR(150) UNIQUE,
        );
    """)

    conn.execute("""
        INSERT INTO dim_arena
        SELECT DISTINCT 
            ROW_NUMBER() OVER () + COALESCE((SELECT MAX(arena_id) FROM dim_arena), 0) AS arena_id,
            arena_city, arena_state, arena_name
        FROM stag_schedules
        WHERE arena_city IS NOT NULL 
            AND arena_state IS NOT NULL 
            AND arena_name IS NOT NULL
        ON CONFLICT(arena_name) DO NOTHING;
    """)

    count = conn.execute("SELECT COUNT(*) FROM dim_arena").fetchone()[0]
    print(f"Tổng số san van dong trong dim_arena: {count}")

    data_table = conn.execute("SELECT * FROM dim_arena").fetchall()

    print(data_table)
    conn.close()

def insert_into_dim_players():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_players (
            player_id INTEGER PRIMARY KEY,
            country_id INTEGER,
            school_id INTEGER,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            full_name VARCHAR(200),
            birth_date DATE,
            height_inches DOUBLE,
            body_weight_lbs DOUBLE,
            jersey VARCHAR(10),
            position VARCHAR(10),
            dleague_flag BOOLEAN,
            nba_flag BOOLEAN,
            games_played_flag BOOLEAN,
            from_year INTEGER,
            to_year INTEGER,
            FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
            FOREIGN KEY (school_id) REFERENCES dim_school(school_id)
        );
    """)

    conn.execute("""
        INSERT INTO dim_players (
            player_id,
            first_name,
            last_name,
            full_name,
            birth_date,
            height_inches,
            body_weight_lbs,
            position,
            country_id,
            school_id,
            from_year,
            to_year,
            nba_flag,
            dleague_flag,
            games_played_flag
        )
        WITH deduplicated_players AS (
            SELECT 
                person_id AS player_id,
                first_name,
                last_name,
                CONCAT_WS(' ', first_name, last_name) AS full_name,
                birth_date,
                height_inches,
                body_weight_lbs,
                CASE 
                    WHEN guard AND forward THEN 'G-F'
                    WHEN forward AND center THEN 'F-C'
                    WHEN guard THEN 'G'
                    WHEN forward THEN 'F'
                    WHEN center THEN 'C'
                    ELSE 'Unknown'
                END AS position,
                country_id,
                school_id,
                from_year,
                to_year,
                nba_flag,
                dleague_flag,
                games_played_flag,
                ROW_NUMBER() OVER (
                    PARTITION BY person_id 
                    ORDER BY to_year DESC NULLS LAST, from_year DESC NULLS LAST
                ) AS rn
            FROM stg_players
            WHERE person_id IS NOT NULL
        )
        SELECT 
            player_id,
            first_name,
            last_name,
            full_name,
            birth_date,
            height_inches,
            body_weight_lbs,
            position,
            country_id,
            school_id,
            from_year,
            to_year,
            nba_flag,
            dleague_flag,
            games_played_flag
        FROM deduplicated_players
        WHERE rn = 1

        ON CONFLICT (player_id) DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            full_name = EXCLUDED.full_name,
            birth_date = EXCLUDED.birth_date,
            height_inches = EXCLUDED.height_inches,
            body_weight_lbs  = EXCLUDED.body_weight_lbs,
            position = EXCLUDED.position,
            country_id = EXCLUDED.country_id,
            school_id = EXCLUDED.school_id,
            from_year = EXCLUDED.from_year,
            to_year = EXCLUDED.to_year,
            nba_flag = EXCLUDED.nba_flag,
            dleague_flag  = EXCLUDED.dleague_flag,
            games_played_flag = EXCLUDED.games_played_flag;
    """)

    count = conn.execute("SELECT COUNT(*) FROM dim_players").fetchone()[0]
    print(f"Tổng số cau thu trong dim_players: {count}")

    data_table = conn.execute("SELECT * FROM dim_players").fetchall()

    print(data_table)
    conn.close()

def insert_into_dim_team():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_team(
            team_league_id INTEGER PRIMARY KEY,
            team_id INTEGER,
            league_id INTEGER,
            city_id INTEGER,
            team_name VARCHAR(100),
            team_abbrev VARCHAR(10),
            season_founded VARCHAR(20),
            season_active_till VARCHAR(20),
            FOREIGN KEY (league_id) REFERENCES dim_league(league_id),
            FOREIGN KEY (city_id) REFERENCES dim_city(city_id)
        );
    """)

    conn.execute("""
        INSERT INTO dim_team (
            team_league_id,
            team_id, 
            league_id,
            city_id, 
            team_name,
            team_abbrev,
            season_founded,
            season_active_till
        )
        SELECT 
            team_league_id,
            team_id,
            league_id,
            city_id,
            team_name,
            team_abbrev,
            season_founded,
            season_active_till
        FROM stg_teams 
        WHERE team_league_id IS NOT NULL
        ON CONFLICT (team_league_id) DO UPDATE SET
            team_id = EXCLUDED.team_id,
            league_id = EXCLUDED.league_id,
            city_id = EXCLUDED.city_id,
            team_name = EXCLUDED.team_name,
            team_abbrev = EXCLUDED.team_abbrev,
            season_founded = EXCLUDED.season_founded,
            season_active_till = EXCLUDED.season_active_till;
    """)
    count = conn.execute("SELECT COUNT(*) FROM dim_team").fetchone()[0]
    print(f"Tổng số doi bong trong dim_team: {count}")

    data_table = conn.execute("SELECT * FROM dim_team").fetchall()

    print(data_table)
    conn.close()

def insert_into_dim_game():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_game (
        game_id INTEGER PRIMARY KEY,
        date_id INTEGER,
        home_team_id INTEGER,
        away_team_id INTEGER,
        arena_id INTEGER,
        game_datetime_est TIMESTAMP,
        game_type VARCHAR(50),
        game_subtype VARCHAR(50),
        game_label VARCHAR(100),
        game_sublabel VARCHAR(100),
        series_game_number INTEGER,
        series_text VARCHAR(100),
        week_number INTEGER,
        officials VARCHAR(255),
        status INTEGER,
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
        FOREIGN KEY (home_team_id) REFERENCES dim_team(team_id),
        FOREIGN KEY (away_team_id) REFERENCES dim_team(team_id),
        FOREIGN KEY (arena_id) REFERENCES dim_arena(arena_id)
    );
    """)