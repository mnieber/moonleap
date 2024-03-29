from moonleap import Prop, extend
from titan.react_pkg.state.resources import State
from titan.types_pkg.item import Item
from titan.types_pkg.itemlist import ItemList
from titan.typespec.field_spec import FieldSpec

from . import props


@extend(Item)
class ExtendItem:
    ts_type = Prop(props.item_ts_type)
    ts_var = Prop(props.item_ts_var)


@extend(ItemList)
class ExtendItemList:
    ts_type = Prop(props.item_list_ts_type)
    ts_var = Prop(props.item_list_ts_var)


@extend(FieldSpec)
class ExtendFieldSpec:
    ts_type = Prop(props.field_spec_ts_type)
    ts_default_value = Prop(props.field_spec_ts_default_value)


@extend(State)
class ExtendState:
    ts_type = Prop(props.state_ts_type)
