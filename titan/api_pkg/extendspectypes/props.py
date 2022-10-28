from moonleap.typespec.field_spec import FieldSpec, FkFieldSpec
from moonleap.typespec.type_spec_store import type_spec_store


def fk_field_spec_target_type_spec(self: FkFieldSpec):
    if not self.target:
        return None

    return type_spec_store().get(self.target)


def form_field_spec_target_type_spec(self: FkFieldSpec):
    if not self.target:
        return None

    return type_spec_store().get(self.target + "Form")


def field_spec_graphql_type(self: FieldSpec, host):
    postfix = "" if self.is_optional(host) else "!"

    if self.field_type in (
        "string",
        "text",
        "json",
        "url",
        "slug",
        "image",
        "markdown",
    ):
        return "String" + postfix

    if self.field_type in ("boolean",):
        return "Boolean" + postfix

    if self.field_type in ("int",):
        return "Int" + postfix

    if self.field_type in ("string[]",):
        return "String[]" + postfix

    if self.field_type in ("int[]",):
        return "Int[]" + postfix

    if self.field_type in ("float",):
        return "Float" + postfix

    if self.field_type in ("uuid",):
        return "ID" + postfix

    if self.field_type in ("uuid[]",):
        return "ID[]" + postfix

    if self.field_type in ("form",):
        return f"{self.target_type_spec.type_name}T" + postfix

    raise Exception(f"Cannot deduce graphql type for {self.field_type}")
