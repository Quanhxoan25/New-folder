CREATE TABLE IF NOT EXISTS dim_country (
    country_id INTEGER PRIMARY KEY,
    country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_school (
    school_id INTEGER PRIMARY KEY,
    school VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_city (
    city_id INTEGER PRIMARY KEY,
    city VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_league (
    league_id INTEGER PRIMARY KEY,
    league VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY, 
    game_day VARCHAR(10),
    season VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS dim_arena (
    arena_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    arena_city VARCHAR(50),
    arena_state VARCHAR(50),
    arena_name VARCHAR(150),
);

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

CREATE TABLE IF NOT EXISTS dim_game (
    game_id INTEGER PRIMARY KEY,
    date_id INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    arena_id INTEGER,
    game_datetime_est TIMESTAMP,
    game_type VARCHAR(50),
    game_sub_type VARCHAR(50),
    game_label VARCHAR(100),
    game_sub_label VARCHAR(100),
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

-- ==========================================
-- FACT TABLES
-- ==========================================

CREATE OR REPLACE TABLE fact_team_statistics (
    game_id INTEGER,
    team_id INTEGER,
    opponent_team_id INTEGER,
    coach_id INTEGER,
    home BOOLEAN,
    win BOOLEAN,
    seed INT,
    team_score INT,
    opponent_score INT,
    plus_minus_points DOUBLE,
    num_minutes INT,
    assists INT,
    blocks INT,
    steals INT,
    turnovers  INT,
    turnovers_team INT,
    fouls_personal INT,
    field_goals_attempted INT,
    field_goals_made INT,
    field_goals_percentage DOUBLE,
    three_pointers_attempted INT,
    three_pointers_made INT,
    three_pointers_percentage DOUBLE,
    free_throws_attempted INT,
    free_throws_made INT,
    free_throws_percentage DOUBLE,
    rebounds_defensive INT,
    rebounds_offensive INT,
    rebounds_total INT,
    rebounds_team INT,
    q1_points INT,
    q2_points INT,
    q3_points INT,
    q4_points INT,
    ot1_points INT,
    ot2_points INT,
    ot_all_points INT,
    bench_points INT,
    points_fast_break INT,
    points_from_turnovers INT,
    points_in_the_paint INT,
    points_second_chance INT,
    biggest_lead INT,
    biggest_scoring_run INT,
    lead_changes INT,
    times_tied INT,
    timeouts_remaining INT,
    season_wins INT,
    season_losses INT,
    PRIMARY KEY (game_id, team_id)
);

CREATE TABLE IF NOT EXISTS fact_team_statistics (
    game_id INTEGER,
    team_id INTEGER,
    date_id INTEGER,
    opponent_team_id INTEGER,
    home BOOLEAN,
    win BOOLEAN,
    team_score INTEGER,
    opponent_score INTEGER,
    assists INTEGER,
    blocks INTEGER,
    steals INTEGER,
    field_goals_attempted INTEGER,
    field_goals_made INTEGER,
    field_goals_percentage DOUBLE,
    three_pointers_attempted INTEGER,
    three_pointers_made INTEGER,
    three_pointers_percentage DOUBLE,
    free_throws_attempted INTEGER,
    free_throws_made INTEGER,
    free_throws_percentage DOUBLE,
    rebounds_defensive INTEGER,
    rebounds_offensive INTEGER,
    rebounds_total INTEGER,
    fouls_personal INTEGER,
    turnovers INTEGER,
    q1_points INTEGER,
    q2_points INTEGER,
    q3_points INTEGER,
    q4_points INTEGER,
    ot1_points INTEGER,
    ot2_points INTEGER,
    ot_all_points INTEGER,
    bench_points INTEGER,
    biggest_lead INTEGER,
    biggest_scoring_run INTEGER,
    lead_changes INTEGER,
    points_fast_break INTEGER,
    points_from_turnovers INTEGER,
    points_in_the_paint INTEGER,
    points_second_chance INTEGER,
    times_tied INTEGER,
    timeouts_remaining INTEGER,
    season_wins INTEGER,
    season_losses INTEGER,
    seed INTEGER,
    rebounds_team INTEGER,
    turnovers_team INTEGER,
    PRIMARY KEY (game_id, team_id, date_id),
    FOREIGN KEY (game_id) REFERENCES dim_game(game_id),
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (opponent_team_id) REFERENCES dim_team(team_id)
);

CREATE TABLE IF NOT EXISTS fact_game_statistics (
    game_id INTEGER PRIMARY KEY,
    date_id INTEGER,
    arena_id INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    winner_team_id INTEGER,
    attendance INTEGER,
    FOREIGN KEY (game_id) REFERENCES dim_game(game_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (arena_id) REFERENCES dim_arena(arena_id),
    FOREIGN KEY (home_team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (away_team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES dim_team(team_id)
);
