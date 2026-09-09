from data_ingestion.ingestion_service import ingest_file
from data_cleaning.cleaning_service import clean_data

from rule_engine.rule_engine_service import run_rules_on_dataframe

from rule_engine.rule_report import (
    generate_rule_report,
    print_rule_report,
    generate_rule_summary,
    print_rule_summary
)


# ============================================================
# INPUT FILE
# ============================================================

file_path = "data/raw/sample_projects.csv"


# ============================================================
# DATA INGESTION
# ============================================================

df = ingest_file(file_path)


if df is not None:

    # ========================================================
    # DATA CLEANING
    # ========================================================

    cleaned_df, duplicate_rows, quality_report = clean_data(df)


    # ========================================================
    # RULE ENGINE
    # ========================================================

    print("\n" + "=" * 60)
    print("RUNNING MPLADS RULE ENGINE")
    print("=" * 60)

    all_results = run_rules_on_dataframe(cleaned_df)


    # ========================================================
    # DETAILED RULE REPORT
    # ========================================================

    rule_report = generate_rule_report(all_results)

    print_rule_report(rule_report)


    # ========================================================
    # PROJECT-LEVEL RULE SUMMARY
    # ========================================================

    rule_summary = generate_rule_summary(rule_report)

    print_rule_summary(rule_summary)