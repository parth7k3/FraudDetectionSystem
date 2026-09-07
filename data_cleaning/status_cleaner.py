import pandas as pd


STATUS_MAPPING = {
    "ongoing": "ONGOING",
    "in progress": "ONGOING",
    "under progress": "ONGOING",
    "work in progress": "ONGOING",

    "completed": "COMPLETED",
    "complete": "COMPLETED",
    "finished": "COMPLETED",

    "not started": "NOT_STARTED",
    "yet to start": "NOT_STARTED",

    "cancelled": "CANCELLED",
    "canceled": "CANCELLED",

    "on hold": "ON_HOLD",
    "hold": "ON_HOLD"
}


def clean_status_values(df):

    if "project_status" not in df.columns:
        return df

    df["project_status"] = df["project_status"].apply(
        normalize_status
    )

    return df


def normalize_status(value):

    if pd.isna(value):
        return pd.NA

    value = str(value).strip().lower()

    return STATUS_MAPPING.get(value, value.upper())
