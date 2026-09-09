import pandas as pd


def generate_rule_report(all_results):

    report_rows = []

    for project in all_results:

        project_id = project.get("project_id")
        project_name = project.get("project_name")

        for result in project["results"]:

            report_rows.append({
                "project_id": project_id,
                "project_name": project_name,
                "rule_id": result.rule_id,
                "status": result.status,
                "reason": result.reason,
                "rule_version": result.rule_version
            })

    return pd.DataFrame(report_rows)


def generate_rule_summary(report_df):

    summary_rows = []

    if report_df.empty:
        return pd.DataFrame(
            columns=[
                "project_id",
                "project_name",
                "total_rules",
                "passed_rules",
                "review_required",
                "overall_status"
            ]
        )

    grouped = report_df.groupby(
        ["project_id", "project_name"],
        dropna=False
    )

    for (project_id, project_name), group in grouped:

        total_rules = len(group)

        passed_rules = (
            group["status"] == "PASS"
        ).sum()

        review_required = (
            group["status"] == "REVIEW_REQUIRED"
        ).sum()

        if review_required > 0:
            overall_status = "REVIEW_REQUIRED"
        else:
            overall_status = "PASS"

        summary_rows.append({
            "project_id": project_id,
            "project_name": project_name,
            "total_rules": total_rules,
            "passed_rules": passed_rules,
            "review_required": review_required,
            "overall_status": overall_status
        })

    return pd.DataFrame(summary_rows)


def print_rule_report(report_df):

    print("\n" + "=" * 70)
    print("MPLADS RULE COMPLIANCE REPORT")
    print("=" * 70)

    if report_df.empty:
        print("No rule results available.")
        return

    print(report_df.to_string(index=False))

    print("=" * 70)


def print_rule_summary(summary_df):

    print("\n" + "=" * 70)
    print("MPLADS RULE SUMMARY")
    print("=" * 70)

    if summary_df.empty:
        print("No rule summary available.")
        return

    print(summary_df.to_string(index=False))

    print("=" * 70)