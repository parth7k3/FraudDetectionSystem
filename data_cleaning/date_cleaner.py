import pandas as pd


DATE_COLUMNS = [
    "start_date",
    "expected_completion_date",
    "actual_completion_date"
]


def clean_date_values(df):

    for column in DATE_COLUMNS:

        if column not in df.columns:
            continue

        df[column] = pd.to_datetime(
            df[column],
            errors="coerce",
            dayfirst=True
        )

    return df