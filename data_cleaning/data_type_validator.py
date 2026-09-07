import pandas as pd


NUMERIC_COLUMNS = [
    "sanctioned_amount",
    "amount_released",
    "amount_spent",
    "completion_percentage"
]


DATE_COLUMNS = [
    "start_date",
    "expected_completion_date",
    "actual_completion_date"
]


def validate_data_types(df):

    for column in NUMERIC_COLUMNS:

        if column not in df.columns:
            continue

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    for column in DATE_COLUMNS:

        if column not in df.columns:
            continue

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df