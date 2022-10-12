from moonleap.typespec.field_spec import get_field_spec_constructor

from .foreign_key import ForeignKey
from .get_fk_field_attrs import get_fk_field_attrs


def get_fk_field_spec(host, fk: ForeignKey, related_name):
    field_attrs = get_fk_field_attrs(
        host,
        fk.var,
        fk.foo,
        fk.bar,
        fk.data_parts,
        fk.target_parts,
    )

    field_spec = get_field_spec_constructor(field_attrs["field_type"])(**field_attrs)
    if field_spec.field_type == "fk" and related_name:
        field_spec.related_name = related_name

    return field_spec
