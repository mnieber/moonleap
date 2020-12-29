from leap_mn.resource import Resource


class Project(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self):
        return {str(self): dict(name=self.name)}


def create(term, line, block):
    return Project(term.data)


create_rule_by_tag = {
    "project": create,
}

is_ittable_by_tag = {
    "project": True,
}