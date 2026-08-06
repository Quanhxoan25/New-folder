from concurrent.futures import ThreadPoolExecutor
import os
from minio import Minio


def get_latest_file(directory: str, extension: str) -> str | None:
    if not os.path.exists(directory):
        return None

    files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(extension)
    ]

    if not files:
        return None
    return max(files, key=os.path.getmtime)


def upload_single_file(
    file_info: tuple[str, str], client: Minio, bucket_name: str
):
    local_path, minio_path = file_info
    try:
        client.fput_object(bucket_name, minio_path, local_path)
        print(f"✅ Upload successfully: {minio_path}")
    except Exception as e:
        print(f"❌ Upload failed [{minio_path}]: {e}")
        raise e


def load_data_to_dl():
    extension = ".parquet"

    # Map thư mục Local với Prefix trên MinIO (dễ quản lý và mở rộng)
    directories_map = [
        (
            "/opt/airflow/elt_pipeline/data/completed/load_api_games_to_parquet",
            "raw/api/games",
        ),
        (
            "/opt/airflow/elt_pipeline/data/completed/load_api_player_stat_to_parquet",
            "raw/api/player_stats",
        ),
        (
            "/opt/airflow/elt_pipeline/data/completed/load_api_schedule_to_parquet",
            "raw/api/schedules",
        ),
        (
            "/opt/airflow/elt_pipeline/data/completed/load_api_team_stat_to_parquet",
            "raw/api/team_stats",
        ),
        (
            "/opt/airflow/elt_pipeline/data/completed/load_db_to_dl/load_player_tb_to_dl",
            "raw/db/players",
        ),
        (
            "/opt/airflow/elt_pipeline/data/completed/load_db_to_dl/load_team_tb_to_dl",
            "raw/db/teams",
        ),
    ]

    file_info = []

    # Kiểm tra an toàn: Chỉ lấy file nếu TỒN TẠI (tránh lỗi NoneType)
    for local_dir, minio_prefix in directories_map:
        latest_file = get_latest_file(local_dir, extension)
        if latest_file:
            minio_path = f"{minio_prefix}/{os.path.basename(latest_file)}"
            file_info.append((latest_file, minio_path))
        else:
            print(
                f"⚠️ Cảnh báo: Bỏ qua vì không tìm thấy file {extension} trong {local_dir}"
            )

    if not file_info:
        print("⚠️ Không có file nào hợp lệ để upload!")
        return

    # Kết nối MinIO nội bộ Docker
    client = Minio(
        "minio:9000",
        access_key="minioadmin",
        secret_key="minioadminpassword",
        secure=False,
    )

    bucket_name = "basketball-data"
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # Upload song song
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(upload_single_file, item, client, bucket_name)
            for item in file_info
        ]

        for future in futures:
            future.result()


if __name__ == "__main__":
    load_data_to_dl()