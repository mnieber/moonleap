from moonleap import MemFun, Prop, extend
from typespec.field_spec import FieldSpec
from typespec.type_spec import TypeSpec

from . import props


@extend(TypeSpec)
class ExtendTypeSpec:
    tn_graphene = Prop(props.tn_graphene)


@extend(FieldSpec)
class ExtendFieldSpec:
    graphene_type = MemFun(props.graphene_type)
    graphql_type = MemFun(props.field_spec_graphql_type)