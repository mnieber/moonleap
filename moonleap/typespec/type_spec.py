import typing as T
from dataclasses import dataclass, field, replace

import ramda as R
from moonleap.typespec.field_spec import FieldSpec
from titan.api_pkg.pkg.ml_name import ml_form_type_name_from_type_name


@dataclass
class TypeSpec:
    type_name: str
    field_specs: T.List[FieldSpec] = field(repr=False)
    select_item_by: T.Optional[T.List[str]] = None
    display_item_by: T.Optional[str] = None
    query_item_by: T.Optional[T.List[str]] = None
    query_items_by: T.Optional[T.List[str]] = None

    def get_field_specs(self, field_types, exclude_names=None):
        return [
            x
            for x in self.field_specs
            if x.field_type in field_types and x.name not in (exclude_names or [])
        ]

    def get_field_spec_by_name(self, field_name):
        return R.head(x for x in self.field_specs if x.name == field_name)


def add_related_set_field_to_type_spec(type_spec, is_private, related_item_name):
    field_name = related_item_name + "Set"
    if [x for x in type_spec.field_specs if x.name == field_name]:
        raise Exception("Field spec with name {name} already exists")

    type_spec.field_specs.append(
        FieldSpec(
            name=field_name,
            required=False,
            private=is_private,
            field_type="relatedSet",
            field_type_attrs=dict(
                target=related_item_name,
            ),
        )
    )


def form_type_spec_from_data_type_spec(data_type_spec):
    def _convert(field_spec):
        changes = {}
        if field_spec.field_type in ("fk",):
            changes = dict(
                name=field_spec.name + "Id",
                field_type="uuid",
                field_type_attrs={"target": field_spec.target},
            )

        return replace(field_spec, **changes)

    return TypeSpec(
        type_name=ml_form_type_name_from_type_name(data_type_spec.type_name),
        field_specs=R.pipe(
            R.always(data_type_spec.field_specs),
            R.filter(lambda x: x.field_type != "relatedSet"),
            R.map(_convert),
        )(None),
    )