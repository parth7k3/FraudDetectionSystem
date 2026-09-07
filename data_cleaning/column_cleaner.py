import re


def clean_column_names(df):
    
    cleaned_columns = []

    for column in df.columns:

        # Convert column name to string
        column = str(column)

        # Remove spaces from beginning and end
        column = column.strip()

        # Convert to lowercase
        column = column.lower()

        # Replace spaces, hyphens and special characters with _
        column = re.sub(r"[^a-z0-9]+", "_", column)

        # Remove _ from beginning and end
        column = column.strip("_")

        cleaned_columns.append(column)

    # Replace original column names
    df.columns = cleaned_columns

    return df