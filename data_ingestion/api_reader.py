import requests
import pandas as pd


def read_api(api_url, params=None, headers=None):

    try:
        response = requests.get(
            api_url,
            params=params,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        # Handles normal JSON lists and nested JSON
        if isinstance(data, list):
            df = pd.DataFrame(data)

        elif isinstance(data, dict):
            df = pd.json_normalize(data)

        else:
            print("Error: Unsupported API response format.")
            return None

        print("API data fetched successfully!")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        return df

    except requests.exceptions.Timeout:
        print("Error: API request timed out.")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")

    except ValueError:
        print("Error: API did not return valid JSON.")

    except Exception as e:
        print(f"Error while reading API data: {e}")

    return None