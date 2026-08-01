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
            PRIMARY KEY (game_id, date_id, player_id),
            FOREIGN KEY (game_id) REFERENCES dim_game(game_id),
            FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
            FOREIGN KEY (player_id) REFERENCES dim_players(player_id)
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
        WHERE (player_team_id = opponent_team_id)
            OR (num_minutes < 0 OR num_minutes > 65 OR points < 0 OR assists < 0 OR blocks < 0 OR steals < 0 OR fouls_personal < 0 OR turnovers < 0)
            OR (starting_position IS NOT NULL 
                AND TRIM(starting_position) <> ''
                AND starting_position NOT IN ('G', 'C', 'F'))
            OR (field_goals_attempted < field_goals_made OR three_pointers_attempted < three_pointers_made OR free_throws_attempted < free_throws_made OR rebounds_defensive > rebounds_total OR rebounds_offensive > rebounds_total )
            OR (three_pointers_attempted > field_goals_attempted)
            OR rebounds_total <> (COALESCE(rebounds_defensive, 0) + COALESCE(rebounds_offensive, 0))
    """)

insert_into_fact_player_statistics()