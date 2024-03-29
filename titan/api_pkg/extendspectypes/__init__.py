from moonleap import MemFun, Prop, extend
from titan.typespec.field_spec import FieldSpec
from titan.typespec.type_spec import TypeSpec

from . import props


@extend(TypeSpec)
class ExtendTypeSpec:
    tn_graphene = Prop(props.tn_graphene)


@extend(FieldSpec)
class ExtendFieldSpec:
    graphene_type = MemFun(props.field_spec_graphene_type)
    graphql_type = Prop(props.field_spec_graphql_type)
