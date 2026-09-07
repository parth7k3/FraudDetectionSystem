import pandas as pd


LOCATION_COLUMNS = [
    "district",
    "state"
]


def clean_location_values(df):

    for column in LOCATION_COLUMNS:

        if column not in df.columns:
            continue

        df[column] = df[column].apply(normalize_location)

    return df


def normalize_location(value):

    if pd.isna(value):
        return pd.NA

    value = str(value).strip()

    value = " ".join(value.split())

    return value.title()
