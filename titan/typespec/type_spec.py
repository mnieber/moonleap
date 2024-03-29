import typing as T
from dataclasses import dataclass, field

import ramda as R
from titan.typespec.field_spec import FieldSpec


@dataclass
class TypeSpec:
    type_name: str
    field_specs: T.List[FieldSpec] = field(repr=False)
    admin_search_by: T.List[str] = field(default_factory=list, repr=False)
    module_name: T.Optional[str] = None
    is_entity: T.Optional[bool] = None
    base_type_name: T.Optional[str] = None
    is_sorted: bool = field(default=False, repr=False)
    is_form: bool = field(default=False, repr=False)
    no_api: bool = field(default=False, repr=False)

    @property
    def only_api(self):
        return not any([x.has_model for x in self.field_specs])

    def get_field_specs(self, field_types=None):
        return [
            x
            for x in self.field_specs
            if (field_types is None or x.field_type in field_types)
        ]

    def get_field_spec_by_key(self, key):
        return R.head(x for x in self.get_field_specs() if x.key == key)

    def add_field_spec(self, field_spec):
        existing_field_spec = self.get_field_spec_by_key(field_spec.key)
        if existing_field_spec:
            raise Exception(f"Duplicate field {field_spec.key} in {self.type_name}")

        self.field_specs.append(field_spec)

    def remove_field_spec_by_key(self, key):
        self.field_specs = [x for x in self.field_specs if x.key != key]
