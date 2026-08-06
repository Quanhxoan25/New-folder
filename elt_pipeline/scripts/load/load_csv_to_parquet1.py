import glob
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def get_latest_file_in_dir(dir_path: str, extension: str = ".json") -> str | None:
    os.makedirs(dir_path, exist_ok=True)

    search_pattern = os.path.join(dir_path, f"*{extension}")
    files = glob.glob(search_pattern)

    if not files:
        return None

    return max(files, key=os.path.getmtime)


def convert_json_to_parquet(
    json_filepath: str, output_filepath: str, chunksize: int = 20000
):
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    if not json_filepath or not os.path.exists(json_filepath):
        print(f"❌ Lỗi: File đầu vào không tồn tại hoặc hợp lệ: {json_filepath}")
        return

    writer = None
    schema = None
    total_rows = 0

    try:
        reader = pd.read_json(
            json_filepath, lines=True, chunksize=chunksize, encoding="utf-8", dtype=str
        )

        for df_chunk in reader:
            if df_chunk.empty:
                continue
            df_chunk = df_chunk.fillna("")
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

            total_rows += len(df_chunk)

        if total_rows == 0:
            print(f"⚠️ Cảnh báo: File không chứa dòng dữ liệu nào: {json_filepath}")
            return

        print(
            f"✅ Đã chuyển đổi thành công {total_rows} dòng sang Parquet: {output_filepath}"
        )

    except ValueError as e:
        print(f"❌ Lỗi đọc file bằng stream: {e}")
        print("💡 Lưu ý: Phương án này yêu cầu file JSON dạng JSON Lines (mỗi dòng 1 record).")

    finally:
        if writer:
            writer.close()


def load_api_to_parquet1():
    input_dir = "/opt/airflow/elt_pipeline/data/raw/player_stats"
    output_dir = "/opt/airflow/elt_pipeline/data/completed/load_api_player_stat_to_parquet"

    # Lấy file .json mới nhất
    input_file = get_latest_file_in_dir(input_dir, extension=".json")

    if not input_file:
        print(f"⚠️ Không tìm thấy file JSON nào trong: {input_dir}")
        return

    # Tự động tạo tên file output (.parquet) từ tên file input
    filename = os.path.basename(input_file)
    file_stem, _ = os.path.splitext(filename)
    output_file = os.path.join(output_dir, f"{file_stem}.parquet")

    CHUNK_SIZE = 20000

    print(f"📖 Đang xử lý file mới nhất: {filename}")
    convert_json_to_parquet(input_file, output_file, chunksize=CHUNK_SIZE)


if __name__ == "__main__":
    load_api_to_parquet1()