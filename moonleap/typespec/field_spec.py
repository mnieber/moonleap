import typing as T
from dataclasses import dataclass, field

from moonleap.utils.case import l0
from moonleap.utils.chop import chop_prefix


@dataclass
class FieldSpec:
    field_type: str
    name: str
    private: bool
    required: bool
    default_value: T.Any = None
    description: T.Optional[str] = None
    unique: bool = False
    field_type_attrs: dict = field(default_factory=dict)

    @property
    def target(self):
        return self.field_type_attrs.get("target")

    @property
    def related_output(self):
        return self.field_type_attrs.get("related_output")

    @property
    def short_name(self):
        return l0(chop_prefix(self.name, self.related_output or ""))


def _default_value(field_spec):
    return field_spec.get("default", None)


def _unique(field_spec):
    return field_spec.get("unique", False)


def _description(field_spec):
    return field_spec.get("description")


def _field_type_and_attrs(field_spec_dict):
    attrs = {}
    t = field_spec_dict.get("type")

    if t == "fk":
        attrs["target"] = field_spec_dict["target"]
        attrs["hasRelatedSet"] = field_spec_dict.get("hasRelatedSet", True)
        if "onDelete" in field_spec_dict:
            attrs["onDelete"] = field_spec_dict["onDelete"]
    elif t == "relatedSet":
        attrs["target"] = field_spec_dict["target"]
    elif t == "form":
        attrs["target"] = field_spec_dict["target"]
    else:
        if "maxLength" in field_spec_dict:
            attrs["maxLength"] = field_spec_dict["maxLength"]

    return t, attrs


def field_specs_from_type_spec_dict(type_spec_dict):
    required = type_spec_dict.get("required", [])
    private = type_spec_dict.get("private", [])
    result = []
    for field_name, field_spec_dict in type_spec_dict["properties"].items():
        t, attrs = _field_type_and_attrs(field_spec_dict)
        if t is None:
            raise Exception(f"Unknown field type for field: {field_name}")

        result.append(
            FieldSpec(
                default_value=_default_value(field_spec_dict),
                description=_description(field_spec_dict),
                field_type=t,
                field_type_attrs=attrs,
                name=field_name,
                private=field_name in private,
                required=field_name in required,
                unique=_unique(field_spec_dict),
            )
        )
    return result


def input_is_used_for_output(input_field_spec, output_field_spec):
    related_output = input_field_spec.related_output
    return not related_output or output_field_spec.name == related_output