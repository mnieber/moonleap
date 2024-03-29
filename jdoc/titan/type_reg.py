import typing as T

from jdoc.moonleap.resource import *
from jdoc.scenario import *


class TypeSpec(Resource):
    pass


class TypeReg(Entity):
    type_specs: T.List[TypeSpec] = []

    def load_type_specs(self):
        pass


global_type_reg = TypeReg()
