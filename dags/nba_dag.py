import sys 
sys.path.append('/opt/airflow')
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from elt_pipeline.scripts.transform.staging import build_stg_teams,build_stg_team_stats, build_stg_schedules, build_stg_players, build_stg_player_stats, build_stg_games 
from elt_pipeline.scripts.transform.dimensions import insert_into_dim_players, insert_into_dim_league,insert_into_dim_team,insert_into_dim_school,insert_into_dim_game,insert_into_dim_date,insert_into_dim_country,insert_into_dim_city,insert_into_dim_arena
from elt_pipeline.scripts.transform.facts import insert_into_game_statistics, insert_into_fact_team_statistics, insert_into_fact_player_statistics

SCRIPTS_DIR = "/opt/airflow/elt_pipeline/scripts"

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    dag_id='nba_elt_pipeline',
    default_args=default_args,
    description='Pipeline ELT xử lý dữ liệu NBA',
    schedule='0 6 * * *',  
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['nba', 'elt'],
) as dag:
    with TaskGroup(group_id='extract_phase') as extract_group:
        crawl_games = BashOperator(
            task_id='crawl_games',
            bash_command=f'python {SCRIPTS_DIR}/extract/crawl_games.py'
        )
        crawl_player_stats = BashOperator(
            task_id='crawl_player_stats',
            bash_command=f'python {SCRIPTS_DIR}/extract/crawl_player_statistics.py'
        )
        crawl_schedule = BashOperator(
            task_id='crawl_schedule',
            bash_command=f'python {SCRIPTS_DIR}/extract/crawl_schedule.py'
        )
        crawl_team_stats = BashOperator(
            task_id='crawl_team_stats',
            bash_command=f'python {SCRIPTS_DIR}/extract/crawl_team_statistics.py'
        )
    with TaskGroup(group_id='load_group') as load_group:
        load_csv1 = BashOperator(
            task_id='load_csv1',
            bash_command=f'python {SCRIPTS_DIR}/load/load_csv_to_parquet1.py'
        )
        load_csv2 = BashOperator(
            task_id='load_csv2',
            bash_command=f'python {SCRIPTS_DIR}/load/load_csv_to_parquet2.py'
        )
        load_db_player = BashOperator(
            task_id='load_db_player',
            bash_command=f'python {SCRIPTS_DIR}/load/load_db_player_tb_to_parquet.py'
        )
        load_db_teams = BashOperator(
            task_id='load_db_teams',
            bash_command=f'python {SCRIPTS_DIR}/load/load_db_teams_tb_to_parquet.py'
        )
        load_to_dl = BashOperator(
            task_id='load_to_dl',
            bash_command=f'python {SCRIPTS_DIR}/load/load_data_to_dl.py'
        )
        [load_db_player, load_csv2, load_db_teams, load_csv1] >> load_to_dl

    with TaskGroup(group_id='staging_phase') as staging_group:
        stg_teams = PythonOperator(task_id='stg_teams', python_callable=build_stg_teams)
        stg_team_stats = PythonOperator(task_id='stg_team_stats', python_callable=build_stg_team_stats)
        stg_schedules = PythonOperator(task_id='stg_schedules', python_callable=build_stg_schedules)
        stg_players = PythonOperator(task_id='stg_players', python_callable=build_stg_players)
        stg_player_stats = PythonOperator(task_id='stg_player_stats', python_callable=build_stg_player_stats)
        stg_games = PythonOperator(task_id='stg_games', python_callable=build_stg_games)
        stg_games >> stg_schedules >> stg_players >> stg_teams >> stg_team_stats >> stg_player_stats

    with TaskGroup(group_id='dimensions_phase') as dimensions_group:
        dim_players = PythonOperator(task_id='dim_players', python_callable=insert_into_dim_players)
        dim_league = PythonOperator(task_id='dim_league', python_callable=insert_into_dim_league)
        dim_team = PythonOperator(task_id='dim_team', python_callable=insert_into_dim_team)
        dim_school = PythonOperator(task_id='dim_school', python_callable=insert_into_dim_school)
        dim_game = PythonOperator(task_id='dim_game', python_callable=insert_into_dim_game)
        dim_date = PythonOperator(task_id='dim_date', python_callable=insert_into_dim_date)
        dim_country = PythonOperator(task_id='dim_country', python_callable=insert_into_dim_country)
        dim_city = PythonOperator(task_id='dim_city', python_callable=insert_into_dim_city)
        dim_arena = PythonOperator(task_id='dim_arena', python_callable=insert_into_dim_arena)
        dim_country >> dim_city >> dim_school >> dim_arena >> dim_league >> dim_date >> dim_players >>dim_team>> dim_game

    with TaskGroup(group_id='facts_phase') as facts_group:
        fact_game_stats = PythonOperator(
            task_id='fact_game_statistics', 
            python_callable=insert_into_game_statistics
        )
        fact_team_stats = PythonOperator(
            task_id='fact_team_statistics', 
            python_callable=insert_into_fact_team_statistics
        )
        fact_player_stats = PythonOperator(
            task_id='fact_player_statistics', 
            python_callable=insert_into_fact_player_statistics
        )
        fact_player_stats >> fact_team_stats >> fact_game_stats
    extract_group >> load_group >> staging_group >> dimensions_group >> facts_group
