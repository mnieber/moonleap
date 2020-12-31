from moonleap.resource import Resource


class Service(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self):
        return {str(self): dict(name=self.name)}


def create(term, block):
    return [Service(term.data)]


is_ittable = True
tags = ["service"]
