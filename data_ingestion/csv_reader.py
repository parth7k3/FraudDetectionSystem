import pandas as pd


def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)

        print("CSV file read successfully!")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        return df

    except FileNotFoundError:
        print("Error: File not found.")

    except Exception as e:
        print(f"Error while reading CSV file: {e}")

    return None