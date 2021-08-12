import moonleap.resource.props as P
from moonleap import extend, kebab_to_camel, kebab_to_snake, tags
from moonleap.verbs import provides
from titan.django_pkg.module import Module

from .resources import ItemType


@tags(["item-type"])
def create_item_type(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    item_type = ItemType(
        name=name,
        name_snake=name_snake,
    )
    return item_type


empty_rules = [("module", provides, "item-type")]


@extend(ItemType)
class ExtendItemType:
    module = P.parent(Module, provides)


@extend(Module)
class ExtendModule:
    item_types = P.children(provides, "item-type")