import os
from datetime import datetime


def generate_file_report(file_path, df, status="SUCCESS"):

    return {
        "source_name": os.path.basename(file_path),
        "source_type": "FILE",
        "file_type": os.path.splitext(file_path)[1]
            .replace(".", "")
            .upper(),

        "total_rows": df.shape[0] if df is not None else 0,
        "total_columns": df.shape[1] if df is not None else 0,

        "column_names": (
            df.columns.tolist()
            if df is not None
            else []
        ),

        "status": status,

        "ingestion_time":
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def generate_api_report(api_url, df, status="SUCCESS"):

    return {
        "source_name": api_url,
        "source_type": "API",
        "file_type": "JSON",

        "total_rows": df.shape[0] if df is not None else 0,
        "total_columns": df.shape[1] if df is not None else 0,

        "column_names": (
            df.columns.tolist()
            if df is not None
            else []
        ),

        "status": status,

        "ingestion_time":
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def print_ingestion_report(report):

    print("\n" + "=" * 45)
    print("INGESTION REPORT")
    print("=" * 45)

    print(f"Source: {report['source_name']}")
    print(f"Source Type: {report['source_type']}")
    print(f"Data Type: {report['file_type']}")
    print(f"Total Rows: {report['total_rows']}")
    print(f"Total Columns: {report['total_columns']}")

    print("\nColumn Names:")

    for column in report["column_names"]:
        print(f"- {column}")

    print(f"\nStatus: {report['status']}")
    print(f"Ingestion Time: {report['ingestion_time']}")

    print("=" * 45)