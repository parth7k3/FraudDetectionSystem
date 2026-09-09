import re

from rule_engine.rule_result import RuleResult
from rule_engine.rule_config import CURRENT_RULE_VERSION


# ============================================================
# POTENTIALLY PROHIBITED WORK CATEGORIES
# ============================================================

PROHIBITED_WORK_PATTERNS = {

    "GOVERNMENT_OFFICE_OR_RESIDENTIAL_BUILDING": [
        r"\bgovernment office\b",
        r"\bgovernment residential building\b",
        r"\bgovernment staff quarters\b",
        r"\bgovernment quarters\b"
    ],

    "PRIVATE_OR_COMMERCIAL_BUILDING": [
        r"\bprivate office\b",
        r"\bprivate residential building\b",
        r"\bcommercial building\b",
        r"\bcommercial establishment\b",
        r"\bcommercial complex\b",
        r"\bshopping complex\b",
        r"\bshopping mall\b"
    ],

    "MAINTENANCE_WORK": [
        r"\bmaintenance\b",
        r"\bannual maintenance\b",
        r"\broutine maintenance\b"
    ],

    "RENOVATION_OR_REPAIR": [
        r"\brenovation\b",
        r"\brenovation work\b",
        r"\brepair work\b",
        r"\brepairing\b"
    ],

    "LAND_ACQUISITION": [
        r"\bland acquisition\b",
        r"\bacquisition of land\b",
        r"\bpurchase of land\b"
    ],

    "REIMBURSEMENT_OF_COMPLETED_WORK": [
        r"\breimbursement\b",
        r"\breimbursement of completed work\b",
        r"\breimbursement of completed works\b"
    ],

    "RECURRING_EXPENDITURE": [
        r"\brecurring expenditure\b",
        r"\bmonthly salary\b",
        r"\bsalary expenditure\b",
        r"\boperational expenses\b"
    ],

    "RELIGIOUS_WORSHIP_PLACE": [
        r"\btemple\b",
        r"\bmosque\b",
        r"\bchurch\b",
        r"\bgurudwara\b",
        r"\bplace of religious worship\b",
        r"\breligious worship\b"
    ]
}


# ============================================================
# EXCEPTION-RELATED TERMS
# ============================================================

EXCEPTION_PATTERNS = {

    "RETROFITTING": [
        r"\bretrofitting\b"
    ],

    "CREMATORIUM": [
        r"\bcrematorium\b",
        r"\bcremation ground\b",
        r"\bburial ground\b"
    ]
}


# ============================================================
# FIND PROHIBITED WORK CATEGORY MATCHES
# ============================================================

def find_matches(description):

    matched_categories = []

    for category, patterns in PROHIBITED_WORK_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, description):

                matched_categories.append(category)
                break

    return matched_categories


# ============================================================
# FIND EXCEPTION-RELATED TERMS
# ============================================================

def find_exceptions(description):

    matched_exceptions = []

    for exception, patterns in EXCEPTION_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, description):

                matched_exceptions.append(exception)
                break

    return matched_exceptions


# ============================================================
# PROHIBITED WORK CHECK
# ============================================================

def check_prohibited_work(project):

    project_name = project.get("project_name")

    # --------------------------------------------------------
    # Missing project description
    # --------------------------------------------------------

    if project_name is None:

        return RuleResult(
            "PROHIBITED_WORK_CHECK",
            "REVIEW_REQUIRED",
            (
                "Project description is missing. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # --------------------------------------------------------
    # Normalize description
    # --------------------------------------------------------

    description = str(project_name).strip().lower()


    # --------------------------------------------------------
    # Find potential prohibited categories
    # --------------------------------------------------------

    matched_categories = find_matches(description)


    # --------------------------------------------------------
    # Find possible exceptions
    # --------------------------------------------------------

    matched_exceptions = find_exceptions(description)


    # --------------------------------------------------------
    # No prohibited category detected
    # --------------------------------------------------------

    if not matched_categories:

        return RuleResult(
            "PROHIBITED_WORK_CHECK",
            "PASS",
            (
                "No potentially prohibited work category was identified. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # --------------------------------------------------------
    # Prohibited category + exception term detected
    # --------------------------------------------------------

    if matched_exceptions:

        return RuleResult(
            "PROHIBITED_WORK_CHECK",
            "REVIEW_REQUIRED",
            (
                "Potentially restricted work category detected: "
                f"{', '.join(matched_categories)}. "

                "An exception-related term was also detected: "
                f"{', '.join(matched_exceptions)}. "

                "Manual verification against the applicable MPLADS "
                "provision is required. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # --------------------------------------------------------
    # Potentially prohibited work detected
    # --------------------------------------------------------

    return RuleResult(
        "PROHIBITED_WORK_CHECK",
        "REVIEW_REQUIRED",
        (
            "Potentially prohibited work category detected: "
            f"{', '.join(matched_categories)}. "

            "Manual verification against the applicable MPLADS "
            "provision is required. "
            f"Rule version: {CURRENT_RULE_VERSION}"
        ),
        CURRENT_RULE_VERSION
    )