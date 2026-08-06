# 🏀 NBA Historical Data ELT Pipeline

Dự án tự động hóa thu thập, lọc và chuẩn hóa dữ liệu lịch sử về các trận đấu, đội bóng và cầu thủ giải bóng rổ nhà nghề Mỹ (NBA) vào Data Warehouse phục vụ cho việc phân tích dữ liệu chuyên sâu.

> 📖 **Tài liệu chi tiết dự án (Notion Document):**  
> Xem thiết kế kiến trúc, luồng xử lý dữ liệu và hướng dẫn chi tiết tại:  
> 👉 [**NBA Data Pipeline Documentation**](https://app.notion.com/p/D-n-Data-Pipeline-l-y-v-ph-n-t-ch-d-li-u-c-u-th-trong-NBA-3a092526d9178085a8dbca4dda15d316?source=copy_link)

---

## 🛠️ Công nghệ sử dụng (Tech Stack)

* **Orchestration:** Apache Airflow
* **Containerization:** Docker & Docker Compose
* **Data Lake Storage:** MinIO (S3 Compatible)
* **Data Engine / DWH:** DuckDB
* **Data Processing:** Python (Pandas, PyArrow, ThreadPoolExecutor)

