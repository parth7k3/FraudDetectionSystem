import os

from data_ingestion.csv_reader import read_csv
from data_ingestion.excel_reader import read_excel
from data_ingestion.json_reader import read_json
from data_ingestion.api_reader import read_api

from data_ingestion.file_validator import validate_file

from data_ingestion.ingestion_report import (
    generate_file_report,
    generate_api_report,
    print_ingestion_report
)


def ingest_file(file_path):

    if not validate_file(file_path):
        return None

    file_extension = os.path.splitext(
        file_path
    )[1].lower()

    print(f"Detected file type: {file_extension}")

    if file_extension == ".csv":
        df = read_csv(file_path)

    elif file_extension == ".xlsx":
        df = read_excel(file_path)

    elif file_extension == ".json":
        df = read_json(file_path)

    else:
        print("Error: Unsupported file format.")
        return None

    if df is not None:

        report = generate_file_report(
            file_path,
            df
        )

        print_ingestion_report(report)

        return df

    return None


def ingest_api(api_url, params=None, headers=None):

    df = read_api(
        api_url,
        params,
        headers
    )

    if df is not None:

        report = generate_api_report(
            api_url,
            df
        )

        print_ingestion_report(report)

        return df

    return None