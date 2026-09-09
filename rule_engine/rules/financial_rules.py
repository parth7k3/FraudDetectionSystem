from rule_engine.rule_result import RuleResult
from rule_engine.rule_config import CURRENT_RULE_VERSION


def check_financial_consistency(project):

    sanctioned = project.get("sanctioned_amount")
    released = project.get("amount_released")
    spent = project.get("amount_spent")


    # ========================================================
    # SANCTIONED AMOUNT
    # ========================================================

    if sanctioned is None:

        return RuleResult(
            "FINANCIAL_CONSISTENCY_CHECK",
            "REVIEW_REQUIRED",
            (
                "Sanctioned amount is missing. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    if sanctioned < 0:

        return RuleResult(
            "FINANCIAL_CONSISTENCY_CHECK",
            "REVIEW_REQUIRED",
            (
                "Sanctioned amount cannot be negative. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # RELEASED AMOUNT
    # ========================================================

    if released is not None and released < 0:

        return RuleResult(
            "FINANCIAL_CONSISTENCY_CHECK",
            "REVIEW_REQUIRED",
            (
                "Released amount cannot be negative. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # SPENT AMOUNT
    # ========================================================

    if spent is not None and spent < 0:

        return RuleResult(
            "FINANCIAL_CONSISTENCY_CHECK",
            "REVIEW_REQUIRED",
            (
                "Spent amount cannot be negative. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # RELEASED > SANCTIONED
    # ========================================================

    if released is not None and released > sanctioned:

        return RuleResult(
            "FINANCIAL_CONSISTENCY_CHECK",
            "REVIEW_REQUIRED",
            (
                "Amount released exceeds the sanctioned amount. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # SPENT > SANCTIONED
    # ========================================================

    if spent is not None and spent > sanctioned:

        return RuleResult(
            "FINANCIAL_CONSISTENCY_CHECK",
            "REVIEW_REQUIRED",
            (
                "Amount spent exceeds the sanctioned amount. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # SPENT > RELEASED
    # ========================================================

    if (
        spent is not None
        and released is not None
        and spent > released
    ):

        return RuleResult(
            "FINANCIAL_CONSISTENCY_CHECK",
            "REVIEW_REQUIRED",
            (
                "Amount spent exceeds the recorded amount released "
                f"for the project. Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # ALL CHECKS PASSED
    # ========================================================

    return RuleResult(
        "FINANCIAL_CONSISTENCY_CHECK",
        "PASS",
        (
            "Financial values are internally consistent. "
            f"Rule version: {CURRENT_RULE_VERSION}"
        ),
        CURRENT_RULE_VERSION
    )