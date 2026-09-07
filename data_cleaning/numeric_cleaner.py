import pandas as pd
import re


NUMERIC_COLUMNS = [
    "sanctioned_amount",
    "amount_released",
    "amount_spent"
]


def clean_numeric_values(df):

    for column in NUMERIC_COLUMNS:

        if column not in df.columns:
            continue

        df[column] = df[column].apply(convert_to_number)

    return df


def convert_to_number(value):

    if pd.isna(value):
        return pd.NA

    value = str(value).strip().lower()

    # Remove currency symbols and commas
    value = value.replace("₹", "")
    value = value.replace("rs.", "")
    value = value.replace("rs", "")
    value = value.replace(",", "")

    # Handle lakh/lakhs
    if "lakh" in value:
        number = re.findall(r"\d+(?:\.\d+)?", value)

        if number:
            return float(number[0]) * 100000

    # Handle crore/crores
    if "crore" in value:
        number = re.findall(r"\d+(?:\.\d+)?", value)

        if number:
            return float(number[0]) * 10000000

    try:
        return float(value)

    except ValueError:
        return pd.NA