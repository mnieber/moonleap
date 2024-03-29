import typing as T
from dataclasses import dataclass, field

from titan.typespec.type_spec import TypeSpec


@dataclass
class ApiSpec:
    name: str
    is_mutation: bool
    inputs_type_spec: TypeSpec = field(repr=False)
    outputs_type_spec: TypeSpec = field(repr=False)
    deletes: T.List[T.Tuple[str, bool]] = field(default_factory=list)  # bool - is_list
    saves: T.List[T.Tuple[str, bool]] = field(default_factory=list)  # bool - is_list
    orders: T.List[T.List[str]] = field(default_factory=list)
    invalidates: T.List[str] = field(default_factory=list)
    is_stub: bool = False
    module_name: str = "api"
    use_in_client: T.Optional[bool] = field(default=None)

    def get_inputs(self, field_types=None):
        return self.inputs_type_spec.get_field_specs(field_types)

    def get_outputs(self, field_types=None):
        return self.outputs_type_spec.get_field_specs(field_types)
