import pandas as pd


def handle_missing_values(df):

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):

            df[column] = df[column].fillna(pd.NA)

        else:

            df[column] = df[column].replace(
                ["", " ", "N/A", "NA", "null", "None", "-"],
                pd.NA
            )

    return df