# Different possible column names mapped to one standard name

COLUMN_MAPPING = {
    "project_name": [
        "project_name",
        "work_name",
        "project_title",
        "name_of_work",
        "work_description"
    ],

    "contractor_name": [
        "contractor_name",
        "contractor",
        "agency_name",
        "implementing_agency",
        "executing_agency"
    ],

    "district": [
        "district",
        "district_name",
        "dist"
    ],

    "state": [
        "state",
        "state_name"
    ],

    "sanctioned_amount": [
        "sanctioned_amount",
        "approved_amount",
        "approved_budget",
        "project_cost",
        "estimated_cost",
        "cost"
    ],

    "amount_released": [
        "amount_released",
        "fund_released",
        "released_amount"
    ],

    "amount_spent": [
        "amount_spent",
        "expenditure",
        "spent_amount",
        "actual_cost"
    ],

    "project_status": [
        "status",
        "project_status",
        "work_status",
        "current_status"
    ],

    "start_date": [
        "start_date",
        "project_start_date",
        "commencement_date",
        "date_of_start"
    ],

    "expected_completion_date": [
        "expected_completion_date",
        "planned_completion_date",
        "target_completion_date",
        "due_date"
    ],

    "actual_completion_date": [
        "actual_completion_date",
        "completion_date",
        "date_of_completion"
    ],

    "completion_percentage": [
        "completion_percentage",
        "progress_percentage",
        "work_progress"
    ],

    "project_id": [
        "project_id",
        "work_id",
        "project_code",
        "project_number"
    ]
}


def map_columns(df):

    rename_mapping = {}

    for standard_name, possible_names in COLUMN_MAPPING.items():

        for column in df.columns:

            if column in possible_names:
                rename_mapping[column] = standard_name
                break

    df = df.rename(columns=rename_mapping)

    return df