from moonleap import u0
from titan.typespec.field_spec import FieldSpec
from titan.typespec.type_spec import TypeSpec


def tn_graphene(self: TypeSpec):
    return f"{u0(self.type_name)}T"


def field_spec_graphene_type(self: FieldSpec, args):
    infix = ", " if args else ""
    if self.field_type == "relatedSet":
        return f"graphene.List({self.target_type_spec.tn_graphene}{infix}{args})"

    if self.field_type == "fk":
        return f"graphene.Field({self.target_type_spec.tn_graphene}{infix}{args})"

    if self.field_type in ("form"):
        return f"{self.target_type_spec.tn_graphene}({args})"

    if self.field_type == "boolean":
        return f"graphene.Boolean({args})"

    if self.field_type == "int":
        return f"graphene.Int({args})"

    if self.field_type == "int[]":
        return f"graphene.List(graphene.Int{infix}{args})"

    if self.field_type == "float":
        return f"graphene.Float({args})"

    if self.field_type in ("string", "text", "slug", "markdown"):
        return f"graphene.String({args})"

    if self.field_type in "string[], tags":
        return f"graphene.List(graphene.String{infix}{args})"

    if self.field_type == "uuid":
        return f"graphene.UUID({args})"

    if self.field_type == "uuid[]":
        return f"graphene.List(graphene.UUID{infix}{args})"

    if self.field_type in ("any", "json"):
        return f"GenericScalar({args})"

    raise Exception(f"Cannot deduce arg type for {self.field_type}")


def field_spec_graphql_type(self: FieldSpec):
    postfix = "" if self.is_optional else "!"

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
        return "[String]" + postfix

    if self.field_type in ("int[]",):
        return "[Int]" + postfix

    if self.field_type in ("float",):
        return "Float" + postfix

    if self.field_type in ("uuid",):
        return "UUID" + postfix

    if self.field_type in ("uuid[]",):
        return "[UUID]" + postfix

    if self.field_type in ("form",):
        return f"{self.target_type_spec.type_name}T" + postfix

    raise Exception(f"Cannot deduce graphql type for {self.field_type}")
