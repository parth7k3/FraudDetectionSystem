from data_cleaning.column_cleaner import clean_column_names
from data_cleaning.schema_mapper import map_columns
from data_cleaning.text_cleaner import clean_text_values
from data_cleaning.missing_value_handler import handle_missing_values
from data_cleaning.numeric_cleaner import clean_numeric_values
from data_cleaning.date_cleaner import clean_date_values
from data_cleaning.location_cleaner import clean_location_values
from data_cleaning.status_cleaner import clean_status_values
from data_cleaning.data_type_validator import validate_data_types
from data_cleaning.duplicate_detector import detect_duplicates
from data_cleaning.data_quality_report import (
    generate_quality_report,
    print_quality_report
)


def clean_data(df):

    print("\nStarting data cleaning...")

    # 1. Clean column names
    df = clean_column_names(df)

    # 2. Map columns to standard schema
    df = map_columns(df)

    # 3. Clean text values
    df = clean_text_values(df)

    # 4. Handle missing values
    df = handle_missing_values(df)

    # 5. Normalize numeric values
    df = clean_numeric_values(df)

    # 6. Normalize dates
    df = clean_date_values(df)

    # 7. Normalize locations
    df = clean_location_values(df)

    # 8. Normalize project status
    df = clean_status_values(df)

    # 9. Validate final data types
    df = validate_data_types(df)

    # 10. Detect duplicates
    duplicate_rows = detect_duplicates(df)

    # 11. Generate quality report
    quality_report = generate_quality_report(df)

    print_quality_report(quality_report)

    print("\nData cleaning completed!")

    return df, duplicate_rows, quality_report
