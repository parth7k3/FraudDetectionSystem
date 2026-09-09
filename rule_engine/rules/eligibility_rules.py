from rule_engine.rule_result import RuleResult
from rule_engine.rule_config import CURRENT_RULE_VERSION


def check_basic_project_eligibility(project):

    required_fields = [
        "project_id",
        "project_name"
    ]

    missing_fields = []

    for field in required_fields:

        if field not in project or project[field] is None:
            missing_fields.append(field)

    if missing_fields:

        return RuleResult(
            "BASIC_PROJECT_ELIGIBILITY",
            "REVIEW_REQUIRED",
            (
                "Missing required project information: "
                f"{', '.join(missing_fields)}"
            ),
            CURRENT_RULE_VERSION
        )

    return RuleResult(
        "BASIC_PROJECT_ELIGIBILITY",
        "PASS",
        (
            "Required project information is available. "
            f"Rule version: {CURRENT_RULE_VERSION}"
        ),
        CURRENT_RULE_VERSION
    )