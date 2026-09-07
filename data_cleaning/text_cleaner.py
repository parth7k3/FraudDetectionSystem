import pandas as pd


# Values that should be treated as missing
MISSING_VALUES = [
    "",
    " ",
    "n/a",
    "na",
    "null",
    "none",
    "not available",
    "not applicable",
    "-"
]


def clean_text_values(df):
    
    for column in df.columns:

        # Only clean text/object columns
        if df[column].dtype == "object":

            # Convert values to strings temporarily
            df[column] = df[column].astype(str)

            # Remove leading/trailing spaces
            df[column] = df[column].str.strip()

            # Replace multiple spaces with a single space
            df[column] = df[column].str.replace(
                r"\s+",
                " ",
                regex=True
            )

            # Convert known missing values to pandas NaN
            df[column] = df[column].replace(
                MISSING_VALUES,
                pd.NA,
                regex=False
            )

    return df
