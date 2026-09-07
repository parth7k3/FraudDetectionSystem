import pandas as pd


def read_excel(file_path):
    try:
        df = pd.read_excel(file_path)

        print("Excel file read successfully!")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        return df

    except FileNotFoundError:
        print("Error: File not found.")

    except Exception as e:
        print(f"Error while reading Excel file: {e}")

    return None