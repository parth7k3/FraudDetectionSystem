import pandas as pd


def detect_duplicates(df):

    duplicate_mask = df.duplicated(
        keep=False
    )

    duplicate_rows = df[duplicate_mask].copy()

    duplicate_count = duplicate_rows.shape[0]

    print("\n" + "=" * 45)
    print("DUPLICATE RECORD CHECK")
    print("=" * 45)

    print(f"Duplicate records found: {duplicate_count}")

    if duplicate_count > 0:
        print("\nDuplicate Records:")
        print(duplicate_rows)

    else:
        print("No duplicate records found.")

    print("=" * 45)

    return duplicate_rows