import pandas as pd


def generate_quality_report(df):

    report = {
        "total_rows": df.shape[0],
        "total_columns": df.shape[1],
        "missing_values": {},
        "duplicate_records": 0,
        "column_types": {}
    }

    # Missing values
    missing_counts = df.isna().sum()

    for column, count in missing_counts.items():

        if count > 0:
            report["missing_values"][column] = int(count)

    # Duplicate records
    report["duplicate_records"] = int(
        df.duplicated().sum()
    )

    # Data types
    for column, dtype in df.dtypes.items():

        report["column_types"][column] = str(dtype)

    return report


def print_quality_report(report):

    print("\n" + "=" * 50)
    print("DATA QUALITY REPORT")
    print("=" * 50)

    print(f"Total Rows: {report['total_rows']}")
    print(f"Total Columns: {report['total_columns']}")

    print("\nMissing Values:")

    if report["missing_values"]:

        for column, count in report["missing_values"].items():
            print(f"- {column}: {count}")

    else:
        print("No missing values.")

    print(
        f"\nDuplicate Records: "
        f"{report['duplicate_records']}"
    )

    print("\nColumn Data Types:")

    for column, dtype in report["column_types"].items():
        print(f"- {column}: {dtype}")

    print("=" * 50)