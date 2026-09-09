from rule_engine.rule_checker import check_rule

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


PROJECT_RULES = [
    check_basic_project_eligibility,
    check_prohibited_work,
    check_financial_consistency
]


def run_project_rules(project):

    results = []

    for rule in PROJECT_RULES:

        result = check_rule(project, rule)

        results.append(result)

    return results


def run_rules_on_dataframe(df):

    all_results = []

    for _, row in df.iterrows():

        project = row.to_dict()

        results = run_project_rules(project)

        all_results.append({
            "project_id": project.get("project_id"),
            "project_name": project.get("project_name"),
            "results": results
        })

    return all_results