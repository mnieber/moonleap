from moonleap import Resource, tags


class PipDependency(Resource):
    def __init__(self, package_names):
        super().__init__()
        self.package_names = package_names


class PipDependencyDev(PipDependency):
    pass


@tags(["pip-dependency"])
def create(term, block):
    return [PipDependency([term.data])]


@tags(["pip-dependency-dev"])
def create(term, block):
    return [PipDependencyDev([term.data])]


meta = {}
