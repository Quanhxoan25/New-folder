
from elt_pipeline.scripts.load.load_data_to_dl import load_data_to_dl
from elt_pipeline.scripts.transform.dimensions import insert_into_dim_arena,insert_into_dim_city,insert_into_dim_country,insert_into_dim_date,insert_into_dim_game,insert_into_dim_league,insert_into_dim_players,insert_into_dim_school,insert_into_dim_team
from elt_pipeline.scripts.transform.staging import build_stg_games, build_stg_player_stats, build_stg_players, build_stg_schedules, build_stg_team_stats, build_stg_teams
from elt_pipeline.scripts.transform.facts import insert_into_fact_player_statistics,insert_into_fact_team_statistics,insert_into_game_statistics 
def run_main_pipeline():
    load_data_to_dl()
    build_stg_games()
    build_stg_schedules() 
    build_stg_players() 
    build_stg_teams()
    build_stg_player_stats()
    build_stg_team_stats() 
    insert_into_dim_country()
    insert_into_dim_school()
    insert_into_dim_league()
    insert_into_dim_city()
    insert_into_dim_date()
    insert_into_dim_arena()
    insert_into_dim_team()
    insert_into_dim_players()
    insert_into_dim_game()
    insert_into_fact_player_statistics()
    insert_into_fact_team_statistics()
    insert_into_game_statistics()

run_main_pipeline()