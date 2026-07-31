import duckdb

def build_stg_games():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("LOAD httpfs")

    conn.execute("""
        CREATE OR REPLACE SECRET minio_secret(
            TYPE s3,
            PROVIDER config,
                KEY_ID 'minioadmin',
                    SECRET 'minioadminpassword',
                    ENDPOINT 'localhost:9000',
                    REGION 'us-east-1',
                    URL_STYLE 'path',
                    USE_SSL false
        )
    """)
    games_path = 's3://basketball-data/raw/api/games/*.parquet'

    raw_data_games= conn.execute(f"SELECT COUNT(*) FROM read_parquet('{games_path}')").fetchone()[0]
    print(f"Data in raw game file: {raw_data_games}")

    conn.execute(f"""
        CREATE OR REPLACE TABLE stag_games AS
        SELECT 
            TRY_CAST(gameId AS INTEGER) AS game_id,
            TRY_CAST(gameDateTimeEst AS TIMESTAMP) AS game_date_time_est,
            NULLIF(TRIM(hometeamCity), '') AS home_team_city,
            NULLIF(TRIM(hometeamName), '') AS home_team_name,
            TRY_CAST(hometeamId AS INTEGER) AS home_team_id,
            NULLIF(TRIM(awayteamCity), '') AS away_team_city,
            NULLIF(TRIM(awayteamName), '') AS away_team_name,
            TRY_CAST(awayteamId AS INTEGER) AS away_team_id,
            TRY_CAST(homeScore AS INTEGER) AS home_score,
            TRY_CAST(awayScore AS INTEGER) AS away_score,
            TRY_CAST(winner AS INTEGER) AS winner_team_id,
            NULLIF(TRIM(gameType), '') AS game_type,
            NULLIF(TRIM(gameSubtype), '') AS game_sub_type,
            NULLIF(TRIM(gameLabel), '') AS game_label,
            NULLIF(TRIM(gameSubLabel), '') AS game_sub_label,
            NULLIF(TRIM(seriesGameNumber), '') AS series_game_number,
            TRY_CAST(attendance AS INTEGER) AS attendance,
            TRY_CAST(arenaId as INTEGER) AS arena_id,
            NULLIF(arenaName, '') AS arena_name,
            NULLIF(TRIM(arenaCity), '') AS arena_city,
            NULLIF(TRIM(arenaState), '') AS arena_state,
            NULLIF(TRIM(officials), '') AS officials,
            TRY_CAST(gameDate AS TIMESTAMP) as game_date
        FROM read_parquet('{games_path}')
    """)
    stagin_count = conn.execute(f"""
        SELECT COUNT(*) FROM stag_games
    """).fetchone()[0]

    print(f"Data in game stag table: {stagin_count}")

build_stg_games()

def build_stg_schedules():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("LOAD httpfs")

    conn.execute("""
        CREATE OR REPLACE SECRET minio_secret(
            TYPE s3,
            PROVIDER config,
                KEY_ID 'minioadmin',
                    SECRET 'minioadminpassword',
                    ENDPOINT 'localhost:9000',
                    REGION 'us-east-1',
                    URL_STYLE 'path',
                    USE_SSL false
        )
    """)

    schedule_path = 's3://basketball-data/raw/api/schedules/*.parquet'
    raw_data_schedules = conn.execute(f"""
        SELECT COUNT(*) FROM read_parquet('{schedule_path}')
    """).fetchone()[0]
    print(f"Data in raw schedules file: {raw_data_schedules}")

    conn.execute(f"""
        CREATE OR REPLACE TABLE stag_schedules AS
        SELECT
            TRY_CAST(gameid AS INTEGER) AS game_id,
            TRY_CAST(gamedatetimeest AS TIMESTAMP) AS game_date_time_est,
            NULLIF(TRIM(gameday), '') AS game_day,
            NULLIF(TRIM(arenacity), '') AS arena_city,
            NULLIF(TRIM(arenastate), '') AS arena_state,
            NULLIF(TRIM(arenaname), '') AS arena_name,
            NULLIF(TRIM(gamelabel), '') AS game_label,
            NULLIF(TRIM(gamesublabel), '') AS game_sub_label,
            NULLIF(TRIM(gamesubtype), '') AS game_sub_type,
            TRY_CAST(gamesequence AS INTEGER) AS game_sequence,
            NULLIF(TRIM(seriesgamenumber), '') AS series_game_number,
            NULLIF(TRIM(seriestext), '') AS series_text,
            TRY_CAST(weeknumber AS INTEGER) AS week_number,
            TRY_CAST(hometeamid AS INTEGER) AS home_team_id,
            TRY_Cast(awayteamid AS INTEGER) AS away_team_id,
            NULLIF(TRIM(season), '') AS season
        FROM read_parquet('{schedule_path}')
    """)

    stag_count = conn.execute("SELECT COUNT(*) FROM stag_schedules").fetchone()[0]
    print(f"Data in schedule stag table: {stag_count}")

build_stg_schedules()

def build_stg_players():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("LOAD httpfs")

    conn.execute("""
        CREATE OR REPLACE SECRET minio_secret(
            TYPE s3,
            PROVIDER config,
                KEY_ID 'minioadmin',
                    SECRET 'minioadminpassword',
                    ENDPOINT 'localhost:9000',
                    REGION 'us-east-1',
                    URL_STYLE 'path',
                    USE_SSL false
        )
    """)
    players_path = 's3://basketball-data/raw/db/players/*.parquet'

    raw_data = conn.execute(
        f"SELECT count(*) FROM read_parquet('{players_path}') LIMIT 10"
    ).fetchone()[0]

    print(f"Data in play stats raw file: {raw_data}")

    conn.execute(f"""
        CREATE OR REPLACE TABLE stg_players AS
        SELECT 
            TRY_CAST(personid AS INTEGER) AS person_id,
            TRY_CAST(countryid as INTEGER) AS country_id,
            NULLIF(TRIM(country), '') AS country,
            TRY_CAST(schoolid AS INTEGER) AS school_id,
            NULLIF(TRIM(school), '') AS school,

            NULLIF(TRIM(firstname), '') AS first_name,
            NULLIF(TRIM(lastname), '') AS last_name,
            TRY_CAST(birthdate AS DATE) AS birth_date,
            TRY_CAST(heightinches AS DOUBLE) AS height_inches,
            TRY_CAST(bodyweightlbs AS DOUBLE) AS body_weight_lbs,

            guard <> 0 AS guard,
            forward <> 0 AS forward,
            center <> 0 AS center, 
            dleagueflag <> 0 AS dleague_flag,
            nbaflag <> 0 AS nba_flag,
            gamesplayedflag <> 0 AS games_played_flag,

            TRY_CAST(fromyear AS INTEGER) AS from_year,
            TRY_CAST(toyear AS INTEGER) AS to_year
        FROM read_parquet('{players_path}')
    """)
    staging_count = conn.execute("""
    SELECT COUNT(*) FROM stg_players
    """).fetchone()[0]

    conn.close()
    print(f"Data in stag player table {staging_count}")

def build_stg_teams():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("LOAD httpfs")

    conn.execute("""
        CREATE OR REPLACE SECRET minio_secret(
            TYPE s3,
            PROVIDER config,
                KEY_ID 'minioadmin',
                    SECRET 'minioadminpassword',
                    ENDPOINT 'localhost:9000',
                    REGION 'us-east-1',
                    URL_STYLE 'path',
                    USE_SSL false
        )
    """)

    team_path = 's3://basketball-data/raw/db/teams/*.parquet'
    raw_data = conn.execute(
        f"SELECT COUNT(*) FROM read_parquet('{team_path}')"
    ).fetchone()[0]

    print(f"Data in play stats raw file: {raw_data}")

    conn.execute(f"""
        CREATE OR REPLACE TABLE stg_teams AS
        SELECT 
            TRY_CAST(team_leagueid AS BIGINT) AS team_league_id,
            TRY_CAST(teamid AS BIGINT) AS team_id,
            TRY_CAST(leagueid AS BIGINT) AS league_id,
            TRY_CAST(cityid AS BIGINT) AS city_id,
            NULLIF(teamname, '') AS team_name,
            NULLIF(teamabbrev, '') AS team_abbrev,
            TRY_CAST(seasonfounded AS INTEGER) AS season_founded,
            TRY_CAST(seasonactivetill AS INTEGER) AS season_active_till,
            NULLIF(city, '') AS city,
            NULLIF(league, '') AS league
        FROM read_parquet('{team_path}')
    """)

    stag_count = conn.execute("SELECT COUNT(*) FROM stg_teams").fetchone()[0]
    data_table = conn.execute("SELECT * FROM stg_teams").fetchall()
    print(f"Data in stag player stats table: {stag_count}")
    print(data_table)

def build_stg_player_stats():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("LOAD httpfs")

    conn.execute("""
        CREATE OR REPLACE SECRET minio_secret(
            TYPE s3,
            PROVIDER config,
                KEY_ID 'minioadmin',
                    SECRET 'minioadminpassword',
                    ENDPOINT 'localhost:9000',
                    REGION 'us-east-1',
                    URL_STYLE 'path',
                    USE_SSL false
        )
    """)

    player_stats_path = 's3://basketball-data/raw/api/player_stats/*.parquet'
    raw_data = conn.execute(
        f"SELECT COUNT(*) FROM read_parquet('{player_stats_path}')"
    ).fetchone()[0]

    print(f"Data in play stats raw file: {raw_data}")

    conn.execute(f"""
        CREATE OR REPLACE TABLE stg_player_stats AS
        SELECT 
            NULLIF(TRIM(firstName), '') AS first_name,
            NULLIF(TRIM(lastName), '') AS last_name,
            TRY_CAST(personId AS INTEGER) AS person_id,
            TRY_CAST(gameId AS INTEGER) AS game_id,
            TRY_CAST(gameDateTimeEst AS TIMESTAMP) AS game_date_time_est,
            NULLIF(TRIM(playerteamCity), '') AS player_team_city,
            NULLIF(TRIM(playerteamName), '') AS player_team_name,
            NULLIF(TRIM(opponentteamCity), '') AS opponent_team_city,
            NULLIF(TRIM(opponentteamName), '') AS opponent_team_name,
            NULLIF(TRIM(gameType), '') AS game_type,
            NULLIF(TRIM(gameLabel), '') AS game_label,
            NULLIF(TRIM(gameSubLabel), '') AS game_sub_label,
            TRY_CAST(seriesGameNumber AS INTEGER) AS series_game_number,
            win <> 0 AS win,
            home <> 0 AS home,
            TRY_CAST(numMinutes AS INTEGER) AS num_minutes,
            TRY_CAST(points AS INTEGER) AS points,
            TRY_CAST(assists AS INTEGER) AS assists,
            TRY_CAST(blocks AS INTEGER) AS blocks,
            TRY_CAST(steals AS INTEGER) AS steals,
            TRY_CAST(fieldGoalsAttempted AS INTEGER) AS field_goals_attemped,
            TRY_CAST(fieldGoalsMade AS INTEGER) AS field_goals_made,
            TRY_CAST(fieldGoalsPercentage AS DOUBLE) AS field_goals_percentage,
            TRY_CAST(threePointersAttempted AS INTEGER) AS three_pointers_attemped,
            TRY_CAST(threePointersMade AS INTEGER) AS three_pointers_made,
            TRY_CAST(threePointersPercentage AS DOUBLE) AS three_pointers_percentage,
            TRY_CAST(freeThrowsAttempted AS INTEGER) AS free_throws_attemped,
            TRY_CAST(freeThrowsMade AS INTEGER) AS free_throws_made,
            TRY_CAST(freeThrowsPercentage AS DOUBLE) AS free_throws_percentage,
            TRY_CAST(reboundsDefensive AS INTEGER) AS rebounds_defensive,
            TRY_CAST(reboundsOffensive AS INTEGER) AS rebounds_offensive,
            TRY_CAST(reboundsTotal AS INTEGER) AS rebounds_total,
            TRY_CAST(foulsPersonal AS INTEGER) AS fouls_personal,
            TRY_CAST(turnovers AS INTEGER) AS turnovers,
            TRY_CAST(plusMinusPoints AS DOUBLE) AS plus_minus_points,
            TRY_CAST(playerteamId AS INTEGER) AS player_team_id,
            TRY_CAST(opponentteamId AS INTEGER) AS opponent_team_id,
            NULLIF(TRIM(comment), '') AS comment,
            NULLIF(TRIM(startingPosition), '') AS starting_position,
            TRY_CAST(gameDate AS TIMESTAMP) AS game_date
        FROM read_parquet('{player_stats_path}')
    """
    )

    stag_count = conn.execute("SELECT COUNT(*) FROM stg_player_stats").fetchone()[0]

    print(f"Data in stag player stats table: {stag_count}")

def build_stg_team_stats():
    duckdb_path = r'D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb'
    conn = duckdb.connect(duckdb_path)

    conn.execute("LOAD httpfs")

    conn.execute("""
        CREATE OR REPLACE SECRET minio_secret(
            TYPE s3,
            PROVIDER config,
                KEY_ID 'minioadmin',
                    SECRET 'minioadminpassword',
                    ENDPOINT 'localhost:9000',
                    REGION 'us-east-1',
                    URL_STYLE 'path',
                    USE_SSL false
        )
    """)

    minio_part = 's3://basketball-data/raw/api/team_stats/*.parquet'
    raw_data = conn.execute(f"SELECT COUNT(*) FROM read_parquet('{minio_part}')").fetchone()[0]
    print(f"Data in raw team stats file: {raw_data}")

    conn.execute(f"""
        CREATE OR REPLACE TABLE stg_team_stats AS
            SELECT
                TRY_CAST(gameId AS BIGINT) AS game_id,
                TRY_CAST(gameDateTimeEst AS TIMESTAMP) AS game_date_time_est,
                NULLIF(TRIM(teamCity), '') AS team_city,
                NULLIF(TRIM(teamName), '') AS team_name,
                TRY_CAST(teamId AS BIGINT) AS team_id,
                NULLIF(TRIM(opponentTeamCity), '') AS opponent_team_city,
                NULLIF(TRIM(opponentTeamName), '') AS opponent_team_name,
                TRY_CAST(opponentTeamId AS BIGINT) AS opponent_team_id,
                home <> 0 AS home,
                win <> 0 AS win,
                TRY_CAST(teamScore AS INT) AS team_score,
                TRY_CAST(opponentScore AS INT) AS opponent_score,
                TRY_CAST(assists AS INT) AS assists,
                TRY_CAST(blocks AS INT) AS blocks,
                TRY_CAST(steals AS INT) AS steals,
                TRY_CAST(fieldGoalsAttempted AS INT) AS field_goals_attempted,
                TRY_CAST(fieldGoalsMade AS INT) AS field_goals_made,
                TRY_CAST(fieldGoalsPercentage AS DOUBLE) AS field_goals_percentage,
                TRY_CAST(threePointersAttempted AS INT) AS three_pointers_attempted,
                TRY_CAST(threePointersMade AS INT) AS three_pointers_made,
                TRY_CAST(threePointersPercentage AS DOUBLE) AS three_pointers_percentage,
                TRY_CAST(freeThrowsAttempted AS INT) AS free_throws_attempted,
                TRY_CAST(freeThrowsMade AS INT) AS free_throws_made,
                TRY_CAST(freeThrowsPercentage AS DOUBLE) AS free_throws_percentage,
                TRY_CAST(reboundsDefensive AS INT) AS rebounds_defensive,
                TRY_CAST(reboundsOffensive AS INT) AS rebounds_offensive,
                TRY_CAST(reboundsTotal AS INT) AS rebounds_total,
                TRY_CAST(foulsPersonal AS INT) AS fouls_personal,
                TRY_CAST(turnovers AS INT) AS turnovers,
                TRY_CAST(plusMinusPoints AS DOUBLE) AS plus_minus_points,
                TRY_CAST(numMinutes AS INT) AS num_minutes,
                TRY_CAST(q1Points AS INT) AS q1_points,
                TRY_CAST(q2Points AS INT) AS q2_points,
                TRY_CAST(q3Points AS INT) AS q3_points,
                TRY_CAST(q4Points AS INT) AS q4_points,
                TRY_CAST(benchPoints AS INT) AS bench_points,
                TRY_CAST(biggestLead AS INT) AS biggest_lead,
                TRY_CAST(biggestScoringRun AS INT) AS biggest_scoring_run,
                TRY_CAST(leadChanges AS INT) AS lead_changes,
                TRY_CAST(pointsFastBreak AS INT) AS points_fast_break,
                TRY_CAST(pointsFromTurnovers AS INT) AS points_from_turnovers,
                TRY_CAST(pointsInThePaint AS INT) AS points_in_the_paint,
                TRY_CAST(pointsSecondChance AS INT) AS points_second_chance,
                TRY_CAST(timesTied AS INT) AS times_tied,
                TRY_CAST(timeoutsRemaining AS INT) AS timeouts_remaining,
                TRY_CAST(seasonWins AS INT) AS season_wins,
                TRY_CAST(seasonLosses AS INT) AS season_losses,
                TRY_CAST(coachId AS BIGINT) AS coach_idd,
                NULLIF(TRIM(gameType), '') AS game_type,
                NULLIF(TRIM(gameLabel), '') AS game_label,
                NULLIF(TRIM(gameSubLabel), '') AS game_sub_label,
                TRY_CAST(seriesGameNumber AS INT) AS series_game_number,
                TRY_CAST(seed AS INT) AS seed,
                TRY_CAST(reboundsTeam AS INT) AS rebounds_team,
                TRY_CAST(turnoversTeam AS INT) AS turnovers_team,
                TRY_CAST(ot1Points AS INT) AS ot1_points,
                TRY_CAST(ot2Points AS INT) AS ot2_points,
                TRY_CAST(otAllPoints AS INT) AS ot_all_points,
                TRY_CAST(gameDate AS DATE) AS game_date
            FROM read_parquet('{minio_part}');
    """)

    stag_count = conn.execute("SELECT COUNT(*) FROM stg_team_stats").fetchone()[0]
    
    print(f"Data in stag player stats table: {stag_count}")


build_stg_teams()