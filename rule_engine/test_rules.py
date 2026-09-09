from rule_engine.rules.eligibility_rules import (
    check_basic_project_eligibility
)

from rule_engine.rules.prohibited_work_rules import (
    check_prohibited_work
)

from rule_engine.rules.financial_rules import (
    check_financial_consistency
)

from rule_engine.rules.allocation_rules import (
    check_sc_st_allocation
)


def test_eligibility_rule():

    print("\nTEST 1: Eligibility Rule")

    project = {
        "project_id": None,
        "project_name": "Road Construction"
    }

    result = check_basic_project_eligibility(project)

    print(result)

    assert result.status == "REVIEW_REQUIRED"

    print("PASS")


def test_prohibited_work_rule():

    print("\nTEST 2: Prohibited Work Rule")

    project = {
        "project_id": "P101",
        "project_name": "Government Office Construction"
    }

    result = check_prohibited_work(project)

    print(result)

    assert result.status == "REVIEW_REQUIRED"

    print("PASS")


def test_financial_rule():

    print("\nTEST 3: Financial Rule")

    project = {
        "project_id": "P102",
        "project_name": "Road Construction",
        "sanctioned_amount": 1000000,
        "amount_released": 1200000,
        "amount_spent": 900000
    }

    result = check_financial_consistency(project)

    print(result)

    assert result.status == "REVIEW_REQUIRED"

    print("PASS")


def test_valid_project():

    print("\nTEST 4: Valid Project")

    project = {
        "project_id": "P103",
        "project_name": "Community Hall",
        "sanctioned_amount": 1000000,
        "amount_released": 800000,
        "amount_spent": 700000
    }

    eligibility = check_basic_project_eligibility(project)
    prohibited = check_prohibited_work(project)
    financial = check_financial_consistency(project)

    assert eligibility.status == "PASS"
    assert prohibited.status == "PASS"
    assert financial.status == "PASS"

    print("PASS")


def test_sc_st_allocation():

    print("\nTEST 5: SC/ST Allocation Rule")

    # Annual entitlement = ₹1 crore
    # SC allocation = 20%
    # ST allocation = 10%
    # Both are above the required minimum.

    result = check_sc_st_allocation(
        total_entitlement=10000000,
        sc_recommended_amount=2000000,
        st_recommended_amount=1000000
    )

    print(result)

    assert result.status == "PASS"

    print("PASS")


def test_sc_st_allocation_review():

    print("\nTEST 6: SC/ST Allocation Review")

    # SC = 10%, below the 15% minimum.
    # ST = 5%, below the 7.5% minimum.

    result = check_sc_st_allocation(
        total_entitlement=10000000,
        sc_recommended_amount=1000000,
        st_recommended_amount=500000
    )

    print(result)

    assert result.status == "REVIEW_REQUIRED"

    print("PASS")


if __name__ == "__main__":

    print("=" * 60)
    print("MPLADS RULE ENGINE TESTS")
    print("=" * 60)

    test_eligibility_rule()
    test_prohibited_work_rule()
    test_financial_rule()
    test_valid_project()
    test_sc_st_allocation()
    test_sc_st_allocation_review()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)