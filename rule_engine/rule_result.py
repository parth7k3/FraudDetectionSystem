from rule_engine.rule_config import CURRENT_RULE_VERSION


class RuleResult:

    def __init__(
        self,
        rule_id,
        status,
        reason,
        rule_version=CURRENT_RULE_VERSION
    ):

        self.rule_id = rule_id
        self.status = status
        self.reason = reason
        self.rule_version = rule_version


    def to_dict(self):

        return {
            "rule_id": self.rule_id,
            "status": self.status,
            "reason": self.reason,
            "rule_version": self.rule_version
        }


    def __str__(self):

        return (
            f"Rule: {self.rule_id}\n"
            f"Status: {self.status}\n"
            f"Reason: {self.reason}\n"
            f"Rule Version: {self.rule_version}"
        )