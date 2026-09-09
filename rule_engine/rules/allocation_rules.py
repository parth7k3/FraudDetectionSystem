from rule_engine.rule_result import RuleResult
from rule_engine.rule_config import CURRENT_RULE_VERSION


SC_MINIMUM_PERCENTAGE = 15.0
ST_MINIMUM_PERCENTAGE = 7.5


def check_sc_st_allocation(
    total_entitlement,
    sc_recommended_amount,
    st_recommended_amount
):

    # ========================================================
    # REQUIRED INPUTS
    # ========================================================

    if total_entitlement is None:

        return RuleResult(
            "SC_ST_ALLOCATION_CHECK",
            "REVIEW_REQUIRED",
            (
                "Annual MPLADS entitlement is missing. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    if sc_recommended_amount is None:

        return RuleResult(
            "SC_ST_ALLOCATION_CHECK",
            "REVIEW_REQUIRED",
            (
                "SC-recommended amount is missing. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    if st_recommended_amount is None:

        return RuleResult(
            "SC_ST_ALLOCATION_CHECK",
            "REVIEW_REQUIRED",
            (
                "ST-recommended amount is missing. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # VALIDATE ENTITLEMENT
    # ========================================================

    if total_entitlement <= 0:

        return RuleResult(
            "SC_ST_ALLOCATION_CHECK",
            "REVIEW_REQUIRED",
            (
                "Annual entitlement must be greater than zero. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # VALIDATE SC/ST AMOUNTS
    # ========================================================

    if sc_recommended_amount < 0 or st_recommended_amount < 0:

        return RuleResult(
            "SC_ST_ALLOCATION_CHECK",
            "REVIEW_REQUIRED",
            (
                "SC/ST recommended amounts cannot be negative. "
                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # CALCULATE ALLOCATION PERCENTAGES
    # ========================================================

    sc_percentage = (
        sc_recommended_amount / total_entitlement
    ) * 100

    st_percentage = (
        st_recommended_amount / total_entitlement
    ) * 100


    # ========================================================
    # CHECK MINIMUM REQUIREMENTS
    # ========================================================

    sc_compliant = (
        sc_percentage >= SC_MINIMUM_PERCENTAGE
    )

    st_compliant = (
        st_percentage >= ST_MINIMUM_PERCENTAGE
    )


    # ========================================================
    # BOTH REQUIREMENTS SATISFIED
    # ========================================================

    if sc_compliant and st_compliant:

        return RuleResult(
            "SC_ST_ALLOCATION_CHECK",
            "PASS",
            (
                f"SC allocation: {sc_percentage:.2f}% "
                f"(required: {SC_MINIMUM_PERCENTAGE}%). "

                f"ST allocation: {st_percentage:.2f}% "
                f"(required: {ST_MINIMUM_PERCENTAGE}%). "

                f"Rule version: {CURRENT_RULE_VERSION}"
            ),
            CURRENT_RULE_VERSION
        )


    # ========================================================
    # COLLECT ALLOCATION ISSUES
    # ========================================================

    issues = []


    if not sc_compliant:

        issues.append(
            f"SC allocation is {sc_percentage:.2f}% "
            f"but minimum is {SC_MINIMUM_PERCENTAGE}%"
        )


    if not st_compliant:

        issues.append(
            f"ST allocation is {st_percentage:.2f}% "
            f"but minimum is {ST_MINIMUM_PERCENTAGE}%"
        )


    # ========================================================
    # REVIEW REQUIRED
    # ========================================================

    return RuleResult(
        "SC_ST_ALLOCATION_CHECK",
        "REVIEW_REQUIRED",
        (
            "; ".join(issues)
            + f". Rule version: {CURRENT_RULE_VERSION}"
        ),
        CURRENT_RULE_VERSION
    )