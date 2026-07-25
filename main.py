import pandas as pd
from pathlib import Path

def merge_schedules_with_schema_drift(output_file):
    df_24_25 = pd.read_csv("D:/HocTap/DATA ENGINEERS/Project/New folder/assets/data/LeagueSchedule24_25.csv")
    df_24_25.columns = df_24_25.columns.str.lower()
    base_column = df_24_25.columns.tolist()

    df_25_26 = pd.read_csv("D:/HocTap/DATA ENGINEERS/Project/New folder/assets/data/LeagueSchedule25_26.csv")
    df_25_26.columns = df_25_26.columns.str.lower()
    df_25_26_cleaned = df_25_26.reindex(columns=base_column)
    
    df_24_25['season'] = "2024-2025"
    df_25_26_cleaned['season'] = "2025-2026"

    df_unified = pd.concat([df_25_26_cleaned,df_24_25], ignore_index=True)
    df_unified.to_csv(output_file, index=False)
    print(f"✅ Gộp thành công! Tổng số hàng: {len(df_unified)}, Tổng số cột: {len(df_unified.columns)}")
    
    return df_unified



df_raw = merge_schedules_with_schema_drift("D:/HocTap/DATA ENGINEERS/Project/New folder/assets/data/schedules_unifield.csv")