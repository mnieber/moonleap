from moonleap.parser.term import fuzzy_match


class Config:
    def __init__(self):
        self.create_rule_by_term = {}
        self.derive_rules_by_resource_type = {}
        self.rules = []

    def get_create_rule(self, subject_term):
        result = None
        for term, rule in config.create_rule_by_term.items():
            if subject_term.tag == term.tag:
                if term.data:
                    if subject_term.data == term.data:
                        return rule
                elif not result:
                    result = rule
        return result

    def get_derive_rules(self, resource_type):
        return self.derive_rules_by_resource_type.get(resource_type) or {}

    def get_rules(self, input_rel, subj_resource, obj_resource):
        return [
            rule
            for rule in self.rules
            if fuzzy_match(input_rel, rule.rel)
            and (not rule.fltr_subj or rule.fltr_subj(subj_resource))
            and (not rule.fltr_obj or rule.fltr_obj(obj_resource))
        ]

    def add_rule(self, rule):
        self.rules.append(rule)


config = Config()
