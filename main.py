import pandas as pd

from data_ingestion.ingestion_service import ingest_file
from data_cleaning.cleaning_service import clean_data


file_path = "data/raw/sample_projects.csv"

df = ingest_file(file_path)

if df is not None:

    print("\nRAW DATA:")
    print(df)

    cleaned_df, duplicate_rows, quality_report = clean_data(df)

    print("\n" + "=" * 50)
    print("FINAL CLEANED DATA")
    print("=" * 50)

    print(cleaned_df)

    print("\n" + "=" * 50)
    print("DUPLICATE ROWS")
    print("=" * 50)

    print(duplicate_rows)