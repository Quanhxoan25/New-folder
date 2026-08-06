import datetime
import os
import pandas as pd


def crawl_player_statistics():
    # 1. Đường dẫn hợp lệ bên trong Docker Container
    csv_path = "/opt/airflow/assets/data/PlayerStatistics.csv"
    print("Start reading player statistics file")

    date = datetime.date.today().strftime("%Y_%m_%d")
    path = f"/opt/airflow/elt_pipeline/data/raw/player_stats/crawl_player_stats_{date}.json"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    chunk_size = 20000

    # Ghi file dạng JSON Lines
    with open(path, "w", encoding="utf-8") as file:
        for chunk in pd.read_csv(
            csv_path,  # 👈 Đã sửa: Dùng biến csv_path thay vì đường dẫn D:\ của Windows
            chunksize=chunk_size,
            low_memory=False,
            dtype=str,  # Ép kiểu str để tránh lỗi xung đột datatype
        ):
            chunk.to_json(file, orient="records", lines=True, force_ascii=False)

    print(f"Data saved to {path}")

    # 2. Đọc kiểm tra: Thêm lines=True và nrows=5 để KHÔNG nạp toàn bộ file vào RAM
    data = pd.read_json(path, lines=True, nrows=5)
    print(data)
    
    


crawl_player_statistics()