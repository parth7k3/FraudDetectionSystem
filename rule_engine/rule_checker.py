from rule_engine.rule_result import RuleResult


def check_rule(project, rule_function):
    result = rule_function(project)

    if not isinstance(result, RuleResult):
        raise TypeError("Rule function must return a RuleResult object.")

    return result