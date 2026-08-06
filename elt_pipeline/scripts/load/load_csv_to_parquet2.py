import json
from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def get_latest_file_in_dir(dir_path: Path, extension: str = ".json"):
    """Tự động kiểm tra/tạo thư mục và lấy file mới nhất."""
    dir_path.mkdir(parents=True, exist_ok=True)
    files = list(dir_path.glob(f"*{extension}"))

    if not files:
        return None

    return max(files, key=lambda f: f.stat().st_mtime)


def save_json_to_parquet_chunked(
    json_filepath: Path, output_filepath: Path, chunksize: int = 20000
):
    """Đọc và ghi file JSON sang Parquet theo từng chunk để tối ưu RAM."""
    output_filepath.parent.mkdir(parents=True, exist_ok=True)

    # Đọc dữ liệu thô từ file JSON
    with open(json_filepath, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    if not raw_data:
        print(f"⚠️ Cảnh báo: File {json_filepath.name} trống.")
        return

    if isinstance(raw_data, dict):
        raw_data = [raw_data]

    total_rows = len(raw_data)
    writer = None
    schema = None

    try:
        for i in range(0, total_rows, chunksize):
            chunk_data = raw_data[i : i + chunksize]

      
            df_chunk = pd.DataFrame(chunk_data)
            df_chunk = df_chunk.convert_dtypes()
            for col in df_chunk.select_dtypes(include=["object"]).columns:
                df_chunk[col] = df_chunk[col].astype("string")

            table_chunk = pa.Table.from_pandas(df_chunk)

            if writer is None:
                schema = table_chunk.schema
                writer = pq.ParquetWriter(
                    output_filepath, schema, compression="snappy"
                )
                writer.write_table(table_chunk)
            else:
                table_chunk = table_chunk.cast(schema)
                writer.write_table(table_chunk)

        print(
            f"✅ Đã ghi thành công {total_rows} dòng vào: {output_filepath.name}"
        )

    finally:
        if writer:
            writer.close()


def load_db_to_dl(
    input_dir_str: str, output_dir_str: str, chunksize: int = 20000
):
    input_dir = Path(input_dir_str)
    output_dir = Path(output_dir_str)

    latest_file = get_latest_file_in_dir(input_dir, extension=".json")

    if latest_file:
        print(f"📖 Đang xử lý file: {latest_file.name}")

        file_name = latest_file.stem + ".parquet"
        output_filepath = output_dir / file_name

        save_json_to_parquet_chunked(
            latest_file, output_filepath, chunksize=chunksize
        )
    else:
        print(f"⚠️ Không tìm thấy file JSON nào trong: {input_dir}")


def load_api_to_parquet2():
    # Danh sách các cặp đường dẫn (Input -> Output)
    pipelines = [
        (
            "/opt/airflow/elt_pipeline/data/raw/games",
            "/opt/airflow/elt_pipeline/data/completed/load_api_games_to_parquet",
        ),
        (
            "/opt/airflow/elt_pipeline/data/raw/schedule",
            "/opt/airflow/elt_pipeline/data/completed/load_api_schedule_to_parquet",
        ),
        (
            "/opt/airflow/elt_pipeline/data/raw/team_stats",
            "/opt/airflow/elt_pipeline/data/completed/load_api_team_stat_to_parquet",
        ),
    ]

    CHUNK_SIZE = 20000

    for input_dir, output_dir in pipelines:
        load_db_to_dl(input_dir, output_dir, chunksize=CHUNK_SIZE)


if __name__ == "__main__":
    load_api_to_parquet2()