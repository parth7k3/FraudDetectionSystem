import pandas as pd


def read_json(file_path):
    try:
        df = pd.read_json(file_path)

        print("JSON file read successfully!")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        return df

    except FileNotFoundError:
        print("Error: File not found.")

    except ValueError as e:
        print(f"Error: Invalid JSON format: {e}")

    except Exception as e:
        print(f"Error while reading JSON file: {e}")

    return None