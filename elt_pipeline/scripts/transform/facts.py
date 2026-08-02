import duckdb

def insert_into_fact_player_statistics ():
    duckdb_path = r"D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb"
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        CREATE OR REPLACE TABLE fact_player_statistics (
            game_id INTEGER,
            date_id INTEGER,
            player_id INTEGER,
            player_team_id INTEGER,
            opponent_team_id INTEGER,
            win BOOLEAN,
            home BOOLEAN,
            starting_position VARCHAR(10),
            comment VARCHAR,
            num_minutes DOUBLE,
            points INTEGER,
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
            plus_minus_points DOUBLE,
            PRIMARY KEY (game_id, player_id)
        );
    """)
    conn.execute("""
        CREATE OR REPLACE TABLE quarantine_player_stats (
            game_id INTEGER,
            date_id INTEGER,
            player_id INTEGER,
            player_team_id INTEGER,
            opponent_team_id INTEGER,
            win BOOLEAN,
            home BOOLEAN,
            starting_position VARCHAR(10),
            num_minutes DOUBLE,
            points INTEGER,
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
            error_reason VARCHAR(255),
            quarantined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        INSERT INTO quarantine_player_stats (
            game_id,
            date_id,
            player_id,
            player_team_id,
            opponent_team_id,
            win,
            home,
            starting_position,
            num_minutes,
            points,
            assists,
            blocks,
            steals,
            field_goals_attempted,
            field_goals_made,
            field_goals_percentage,
            three_pointers_attempted,
            three_pointers_made,
            three_pointers_percentage,
            free_throws_attempted,
            free_throws_made,
            free_throws_percentage,
            rebounds_defensive,
            rebounds_offensive,
            rebounds_total,
            fouls_personal,
            turnovers,
            error_reason
        )
        SELECT 
            game_id,
            COALESCE(
                CAST(STRFTIME(game_date_time_est, '%Y%m%d') AS INTEGER),
                -1
            ) AS date_id, 
            person_id AS player_id,
            player_team_id,
            opponent_team_id,
            win,
            home,
            starting_position,
            num_minutes,
            points,
            assists,
            blocks,
            steals,
            field_goals_attempted,
            field_goals_made,
            field_goals_percentage,
            three_pointers_attempted,
            three_pointers_made,
            three_pointers_percentage,
            free_throws_attempted,
            free_throws_made,
            free_throws_percentage,
            rebounds_defensive,
            rebounds_offensive,
            rebounds_total,
            fouls_personal,
            turnovers,
            CASE
                WHEN person_id IS NULL
                    THEN 'Loi: person_id key khong co gia tri'
                WHEN player_team_id = opponent_team_id 
                    THEN 'Lỗi: player_team_id trùng với opponent_team_id'

                WHEN num_minutes < 0 OR num_minutes > 65 
                    THEN 'Lỗi: Số phút thi đấu không hợp lệ (< 0 hoặc > 65 phút)'

                WHEN points < 0 OR assists < 0 OR blocks < 0 OR steals < 0 OR fouls_personal < 0 OR turnovers < 0 
                    THEN 'Lỗi: Có chỉ số thống kê bị âm'

                WHEN starting_position IS NOT NULL 
                    AND TRIM(starting_position) <> '' 
                    AND starting_position NOT IN ('G', 'C', 'F') 
                    THEN 'Lỗi: Vị trí xuất phát (starting_position) không hợp lệ'

                WHEN field_goals_attempted < field_goals_made 
                OR three_pointers_attempted < three_pointers_made 
                OR free_throws_attempted < free_throws_made 
                    THEN 'Lỗi: Số cú ném trúng (Made) lớn hơn số cú ném thử (Attempted)'

                WHEN three_pointers_attempted > field_goals_attempted 
                    THEN 'Lỗi: Số cú ném 3 điểm vượt quá tổng số cú ném trường (FG)'

                WHEN rebounds_defensive > rebounds_total 
                OR rebounds_offensive > rebounds_total 
                    THEN 'Lỗi: Rebound phòng thủ/tấn công lớn hơn Rebound tổng'

                WHEN COALESCE(rebounds_total, 0) <> (COALESCE(rebounds_defensive, 0) + COALESCE(rebounds_offensive, 0)) 
                    THEN 'Lỗi: Rebound tổng không bằng (Rebound phòng thủ + Tấn công)'
                ELSE 'Valid'
            END AS error_reason
        FROM stg_player_stats
        WHERE person_id IS NULL
            OR (player_team_id = opponent_team_id)
            OR (num_minutes < 0 OR num_minutes > 65 OR points < 0 OR assists < 0 OR blocks < 0 OR steals < 0 OR fouls_personal < 0 OR turnovers < 0)
            OR (starting_position IS NOT NULL 
                AND TRIM(starting_position) <> ''
                AND starting_position NOT IN ('G', 'C', 'F'))
            OR (field_goals_attempted < field_goals_made OR three_pointers_attempted < three_pointers_made OR free_throws_attempted < free_throws_made OR rebounds_defensive > rebounds_total OR rebounds_offensive > rebounds_total )
            OR (three_pointers_attempted > field_goals_attempted)
            OR rebounds_total <> (COALESCE(rebounds_defensive, 0) + COALESCE(rebounds_offensive, 0))
    """)
    conn.execute("""
        INSERT INTO fact_player_statistics (
            game_id ,
            date_id ,
            player_id ,
            player_team_id ,
            opponent_team_id ,
            win ,
            home ,
            starting_position,
            comment ,
            num_minutes,
            points ,
            assists ,
            blocks ,
            steals ,
            field_goals_attempted ,
            field_goals_made ,
            field_goals_percentage,
            three_pointers_attempted ,
            three_pointers_made ,
            three_pointers_percentage,
            free_throws_attempted,
            free_throws_made ,
            free_throws_percentage,
            rebounds_defensive ,
            rebounds_offensive ,
            rebounds_total ,
            fouls_personal ,
            turnovers,
            plus_minus_points
        )
        SELECT 
            s.game_id ,
            COALESCE(
                CAST(STRFTIME(s.game_date_time_est, '%Y%m%d') AS INTEGER),
                -1
            ) AS date_id,
            s.person_id,
            s.player_team_id,
            s.opponent_team_id,
            s.win,
            s.home,
            s.starting_position,
            s.comment ,
            s.num_minutes,
            s.points,
            s.assists ,
            s.blocks ,
            s.steals ,
            s.field_goals_attempted ,
            s.field_goals_made ,
            s.field_goals_percentage,
            s.three_pointers_attempted ,
            s.three_pointers_made ,
            s.three_pointers_percentage,
            s.free_throws_attempted,
            s.free_throws_made ,
            s.free_throws_percentage,
            s.rebounds_defensive ,
            s.rebounds_offensive ,
            s.rebounds_total ,
            s.fouls_personal ,
            s.turnovers,
            s.plus_minus_points
        FROM stg_player_stats s
        WHERE s.person_id IS NOT NULL AND
            NOT EXISTS (
            SELECT 1 FROM quarantine_player_stats q
            WHERE q.game_id = s.game_id 
                AND q.player_id = s.person_id
        )
        ON CONFLICT (game_id, player_id) DO NOTHING;
    """)
    stag_table = conn.execute("SELECT COUNT(*) FROM stg_player_stats").fetchone()[0]
    quarantive_table = conn.execute("SELECT COUNT(*) FROM quarantine_player_stats").fetchone()[0]
    fact_table = conn.execute("SELECT COUNT(*) FROM fact_player_statistics").fetchone()[0]

    print(f"{fact_table} = {stag_table} - {quarantive_table}")

def insert_into_fact_team_statistics():
    duckdb_path = r"D:\HocTap\DATA ENGINEERS\Project\New folder\warehouse\datawarehouse.duckdb"
    conn = duckdb.connect(duckdb_path)

    conn.execute("""
        CREATE OR REPLACE TABLE fact_team_statistics (
            game_id INTEGER,
            team_id INTEGER,
            opponent_team_id INTEGER,
            coach_id INTEGER,
            game_id INTEGER,
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
            season_losses INT
        );
    """)